def filter_header(header: str) -> str:
    lignes = header.splitlines()
    output = []
    in_macro = False  
    for ligne in lignes:
        stripped = ligne.strip()
        if not stripped:
            continue
        if in_macro:
            if not stripped.endswith("\\"):
                in_macro = False  
            continue
        if stripped.startswith("#"):

            if stripped.endswith("\\"):
                in_macro = True
            continue  
        words = stripped.split()
        if words and words[0] == "extern":
            continue
        output.append(ligne)
    return "\n".join(output)