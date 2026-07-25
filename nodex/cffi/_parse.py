import re

def read_cdef_body(path: str) -> str:
    with open(path, "r") as f:
        content = f.read()

    match = re.search(r"^\s*#\s*define\s+END_PREPROCESSOR\s*$", content, re.MULTILINE)
    if match is None:
        return content

    return content[match.end():].lstrip("\n")
