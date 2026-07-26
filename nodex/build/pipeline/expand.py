from pathlib import Path
import re

def expand_includes(file_path: Path, project_root: Path, visited: set = None, ignored_keywords: list[str] = None) -> str:
    if visited is None:
        visited = set()
    if ignored_keywords is None:
        ignored_keywords = ["raylib"]
    file_path = file_path.resolve()
    project_root = project_root.resolve()
    if file_path in visited:
        return ""
    if not file_path.exists():
        print(f"[ATTENTION] Fichier introuvable : {file_path}")
        return ""
    visited.add(file_path)
    content = file_path.read_text(encoding="utf-8")
    result = []
    for line in content.splitlines():
        match = re.match(r'^\s*#include\s*(["<])([^">]+)[">]', line)
        if match:
            delimiter = match.group(1)
            inc_file = match.group(2)
            if delimiter == "<":
                result.append(line)
                continue
            if any(kw in inc_file for kw in ignored_keywords):
                continue
            target_path = (file_path.parent / inc_file).resolve()
            if not target_path.exists():
                target_path = (project_root / inc_file).resolve()
            if target_path.exists():
                result.append(
                    expand_includes(
                        target_path, project_root, visited, ignored_keywords
                    )
                )
            else:
                print(
                    f"[ATTENTION] Include non résolu : '{inc_file}' depuis {file_path.name}"
                )
            continue
        result.append(line)
    return "\n".join(result)