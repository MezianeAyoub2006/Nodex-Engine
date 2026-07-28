import nodex


@nodex.compile("include/bullet.h") # si besoin de la définition C 
# ou
@nodex.compile()
class Bullet(nodex.Node): # entitée enregistrée via __name__ 
    def __init__(self, context, init_x: float, init_y: float, init_dx: float, init_dy: float):  # context bas niveau   
        super().__init__(context) # la classe Node a été changée, ce __init__ context
        # fait essentiollement self.context = context, donc pareil que l'API haut niveau
        # mais c'est une illusion.
        self.tex = self.context.assets.load_image("player.png") # pareil, ici l'utilisateur a l'impression 
        # d'utiliser l'API haut niveau
        self.other_tex = self.context.assets.load_image("hello_world.png") 
        self.x = init_x 
        self.y = init_y
        self.dx = init_dx   
        self.dy = init_dy
      
    def update(self):
        self.x += self.dx * self.context.dt 
        self.y += self.dy * self.context.dt
        self.context.draw(self.tex, (self.x, self.y)) # dispach statique selon le type d'objet 

        self.context.Nx_StartProfile("label") # acces a l'api réele 
        for i in range(10):
            self.context.draw(
                self.other_tex, 
                (self.x + i, self.y), 
                profiling_label = "label"
            ) # support des parametres optionnels (mis a NULL sinin)     
        self.context.Nx_EndProfile() 

# structure d'une entitée interne au moteur (simplifiée)

"""
typedef struct {
    void (*update)(NxEntity* self); 
    void (*init)(NxEntity* self); 
    void* data; 
} NxEntity; 
"""

#Traduction en C: 

"""
#include "nodex.h" 

typedef struct {
    float x; 
    float y; 
    float dx; 
    float dy; 
    NxTexture tex; 
    NxTexture other_tex; 
} __Nx_Bullet; 

void __Nx_Bullet_init(NxEntity* self, float init_x, float init_x, float init_dx, float init_dy) {
    __Nx_Bullet rSelf = (__Nx_Bullet*)(self->data); 
    r-
    rSelf->x = init_x; 
    rSelf->dx = init_x; 
    rSelf->y = init_dx; 
    rSelf->dy = init_dy; 
}

...


"""