import os
from cffi import FFI

def build_cffi_module(module_name: str, c_file: str, h_file: str):
    ffibuilder = FFI()

    # 1. Lecture du fichier header (.h)
    with open(h_file, "r", encoding="utf-8") as f:
        header_content = f.read()

    # 2. cdef() prend les signatures C (CFFI ne supporte pas les directives #include ici, 
    # juste les déclarations de structures et de fonctions)
    ffibuilder.cdef(header_content)

    # 3. set_source() associe le nom du module Python final et inclut le code C réel
    with open(c_file, "r", encoding="utf-8") as f:
        c_code = f.read()

    ffibuilder.set_source(
        f"_{module_name}",  # Nom du module compilé (ex: _my_math)
        f"""
        #include "{os.path.basename(h_file)}"
        """,
        sources=[c_file],    # Fichier source C à compiler
        libraries=[]         # Tu peux ajouter des libs tierces ici si besoin (ex: ['opengl32'])
    )

    # 4. Compilation du module
    print(f"[CFFI] Compilation de {module_name}...")
    ffibuilder.compile(verbose=True)
    print(f"[CFFI] Module _{module_name} compilé avec succès !")

if __name__ == "__main__":
    # Exemple d'utilisation :
    build_cffi_module(
        module_name="add_module",
        c_file="add.c",
        h_file="add.h"
    )