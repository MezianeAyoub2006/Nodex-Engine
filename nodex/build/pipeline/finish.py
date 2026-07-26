from pathlib import Path

def pipeline_end(filtered_header: str) -> str: 
    filtered_header_lines = filtered_header.splitlines()
    with open(Path(__file__).parent / "custom.h", "r") as file: 
        custom = file.read()
    custom_lines = custom.splitlines()
    return "\n".join(custom_lines + filtered_header_lines)