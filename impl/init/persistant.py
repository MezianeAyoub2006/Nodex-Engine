import nodex
import impl
import pygame

from .viewport import ViewportLoader
from .asset import AssetLoader

MOUSE_OFFSET = (-5, -2)

class Persistant(nodex.GameNode):
    def __init__(self, context: "nodex.Context", display_fps = False):
        super().__init__(context)
        self.context.fonts.load_sys_font("consolas", "consolas", (16,))
        self.context.fonts.load_font("main", "assets/fonts/main.ttf", (16,))
        self.context.shaders.load("fx", "shaders/fx.glsl")
        self.context.shaders.load("filter", "shaders/filter.glsl")
        self.context.post_process.register_effect("fx", self.context.shaders.get("fx"))
        self.context.post_process.register_effect("filter", self.context.shaders.get("filter"))
        self.context.input.mouse_set_visible(False)
        self.context.globals["key_profile"] = "WASD"

        self.intro = impl.IntroHandler(context)    
        self.sky = impl.Sky(self.context)

        self._load()
        self.context.post_process.enable_effect("filter")

        self.display_fps = display_fps

    def load_material_map(self):
        img = self.context.assets.get_image("materials")
        self.context.globals["materials_map"] = pygame.surfarray.array3d(img)
        self.context.globals["materials_map_size"] = img.get_size()  
        

    def _load(self):
        AssetLoader(self.context).load()
        ViewportLoader(self.context).load()
        self.load_material_map()
        self._load_scenes()
        self._load_game_nodes()

    def _load_scenes(self):
        for name in ("pygame", "moderngl", "menu", "main", "quit", "settings"):
            self.context.scenes.add_scene(name)

    def _load_game_nodes(self):
        self.context.scenes.persistant.add_game_node(self)
        self.context.scenes["menu"].add_game_node(impl.MenuScene(self.context))
        self.context.scenes["main"].add_game_node(impl.GameScene(self.context))
        self.context.scenes["main"].add_game_node(impl.Hub(self.context))
        self.context.scenes["menu"].add_game_node(impl.Hub(self.context))
        self.context.scenes["quit"].add_game_node(impl.QuitScene(self.context))
        self.context.scenes["settings"].add_game_node(impl.Hub(self.context))
        self.context.scenes["settings"].add_game_node(impl.SettingsScene(self.context))
        self.context.scenes.switch("pygame") 
    
    def display_mouse(self):
        mouse_pos = self.context.input.mouse_position
        if self.context.scenes.current_scene in ("menu", "settings"):
            self.context.overlay.draw(
                "mouse", f"mouse.{int(self.context.input.mouse_pressed[0])}.{0}", position = (
                mouse_pos[0] + MOUSE_OFFSET[0],
                mouse_pos[1] + MOUSE_OFFSET[1]
            ))

    def update(self):
        self.context.overlay.viewports["text"].set_uniform("color", nodex.Color.WHITE)
        cam = self.context.renderer.camera3D("mode7")
        if self.context.scenes.current_scene in ("menu", "main", "settings"):
            self.sky.update(cam)
        if self.context.scenes.current_scene in ("menu", "settings"):
            cam.position.x = 0.5
            cam.position.y = 0.5
            cam.position.z = 0.1 
            cam.rotation += self.context.dt * 0.3
            self.context.renderer.draw("mode7", "ground")
        if self.display_fps:
            text = self.context.fonts.render("main16", str(round(self.context.fps)))
            self.context.overlay.draw("text", text, position=(3, 0))
        self.intro.update()
        self.display_mouse()
