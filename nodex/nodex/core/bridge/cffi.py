from ....build import cffi

class Cffi:
    def __init__(self):
        self.ffi = cffi.ffi 
        self.lib = cffi.lib 

    def to_string(self, cdata_char_s):
        if cdata_char_s == self.ffi.NULL:
            return ""
        
        # On récupère les bytes bruts via CFFI
        raw_bytes = self.ffi.string(cdata_char_s)
        
        # Tentative en UTF-8, si un octet est invalide (comme 0xad), 
        # on le remplace par un caractère de remplacement Unicode () 
        # ou on utilise 'ignore' pour le sauter.
        return raw_bytes.decode('utf-8', errors='replace')