import nodex

class AssetLoader:
    def __init__(self, context : "nodex.Context"):
        self.context = context

    def load(self):
        a = self.context.assets
        s = self.context.sounds
        a.load_image("ground", "assets/images/grounds/main3.png")
        a.load_image("materials", "assets/images/grounds/materials.png")
        a.load_image("title", "assets/images/ui/title.png")
        a.load_image("fx", "assets/images/ui/fx.png")
        a.load_image("sky", "assets/images/background/sky.png")
        a.load_image("pygame", "assets/images/ui/pygame-logo.png")
        a.load_image("moderngl", "assets/images/ui/moderngl-logo.png")
        a.load_image("parallax0", "assets/images/background/parallax0.png")
        a.load_image("parallax1", "assets/images/background/parallax1.png")
        a.load_spritesheet("clouds", "assets/images/background/clouds.png", (32, 16))
        a.load_spritesheet("flower", "assets/images/billboard/spritestack/flower.png", (28, 47))
        a.load_spritesheet("bloc", "assets/images/billboard/spritestack/bloc.png", (28, 47))
        a.load_spritesheet("sign", "assets/images/billboard/spritestack/sign.png", (56, 95))
        a.load_spritesheet("ice0", "assets/images/billboard/spritestack/ice0.png", (56, 95))
        a.load_spritesheet("ice1", "assets/images/billboard/spritestack/ice1.png", (112, 190))
        a.load_spritesheet("buttons", "assets/images/ui/buttons.png", (128, 32))
        a.load_spritesheet("player", "assets/images/billboard/flat/player.png", (32, 32))
        a.load_spritesheet("tree", "assets/images/billboard/spritestack/tree.png", (112, 270))
        a.load_spritesheet("drift", "assets/images/billboard/spritestack/drift.png", (112, 190))
        a.load_spritesheet("jump", "assets/images/billboard/spritestack/jump.png", (112, 190))
        a.load_image("island", "assets/images/background/island.png")
        a.load_image("boats", "assets/images/background/boats.png")
        a.load_image("iceberg", "assets/images/background/iceberg.png")
        a.load_image("iceberg1", "assets/images/background/iceberg1.png")
        a.load_image("iceberg2", "assets/images/background/iceberg2.png")
        a.load_image("forest", "assets/images/background/forest.png")
        a.load_spritesheet("mouse", "assets/images/ui/mouse.png", (16, 16))
        a.load_image("temp", "assets/images/ui/temp.png")
        a.load_spritesheet("nums", "assets/images/ui/nums.png", (24, 24))
        a.load_image("player_ice", "assets/images/billboard/flat/ice.png")
        a.load_image("minimap", "assets/images/ui/minimap.png")
        s.load_sound("button", "assets/sounds/sfx/button.wav")
        s.load_sound("jump", "assets/sounds/sfx/jump.wav")
        s.load_sound("freeze", "assets/sounds/sfx/hit.wav")
        s.load_sound("score", "assets/sounds/sfx/score.wav")
        s.load_sound("hit", "assets/sounds/sfx/freeze.wav") 
        s.load_sound("respawn", "assets/sounds/sfx/respawn.wav")
        s.load_sound("winter-waltz", "assets/sounds/ost/winter-waltz.mp3")
        s.load_sound("race", "assets/sounds/ost/race.mp3")
        s.load_sound("winter-turning", "assets/sounds/ost/winter-turning.mp3")
        s.load_sound("pygame", "assets/sounds/ost/pygame.wav")
        s.load_sound("moderngl", "assets/sounds/ost/modern.wav")
  
  