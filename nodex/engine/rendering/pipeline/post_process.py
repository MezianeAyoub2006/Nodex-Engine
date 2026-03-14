import nodex

class PostProcess:
    def __init__(self, context : "nodex.Context"):
        self.context = context 
        self.active_effects = set()
    
    def register_effect(self, name, frag_prog):
        self.context._gl_context.register_effect(name, frag_prog) 

    def set_uniform(self, effect_name, uniform_name, value):
        self.context._gl_context.set_uniform(effect_name, uniform_name, value)

    def enable_effect(self, effect_name):
        self.context._gl_context.post_process.add(effect_name)
    
    def diseable_effect(self, effect_name):
        if effect_name in self.context._gl_context.post_process:
            self.context._gl_context.post_process.remove(effect_name)


    
