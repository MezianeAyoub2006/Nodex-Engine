import nodex
import pygame

from .world_pass import WorldPass
from .shader_pass import ShaderPass
from .pygame_pass import PygamePass

class Mode7Pass:
    def __init__(self, context : "nodex.Context", settings):
        """ 
        The Mode 7 is a type of projection where a ground texture is projected in a 3D space 
        My implementation uses two shader passes, a dynamic_pass, that stores a pygame surface
        that can be modified (blit into)
        And a static one, that just stores a texture.
        I did that because blitting into a big pygame surface is expensive, I don't want to 
        sacrifize the world size, or performance of the game, so reduced the performance cost
        of the most expensive system (pygame.Surface.blit)

        This layer contains two cameras, a global 3D, and local 2D camera inside the dynamic pass
        (it's a world pass), I did it to synchronize the rendering between the two textures.
        """

        self.context = context

        self.camera = nodex.Camera3D()
        # static texture shader pass 
        self.static_pass = ShaderPass(self.context, self.context.shaders.get("_mode7")) 
        # we load it's texture from the settings
        self.static_pass.load_texture(settings["texture_name"], settings["texture"])
        print(settings["infinite"])
        self.static_pass.load_texture("infinite", settings["infinite"])
        self.static_pass.load_texture("extra", settings["extra"])
        
        # dynamic texture shader pass
        self.dynamic_pass = WorldPass(self.context, self.context.shaders.get("_mode7"))
        self.dynamic_pass.load_texture("infinite", settings["infinite"])
        self.dynamic_pass.load_texture("extra", settings["extra"])
 
        self.camera.position.z = 0.1
        self.camera.position.x = 0.5
        self.camera.position.y = -0.3


        self.scenes = settings["scenes"]

    @property
    def static_size(self):
        """
        Returns the size of the static texture.
        """
        return self.static_pass.textures["tex"][0].size

    @property
    def dynamic_size(self):
        """
        Returns the size of the dynamic texture.
        """
        return self.dynamic_pass.textures["tex"][0].size

    @property
    def scale(self):
        """ 
        Returns the ratio between the static, and dynamic texture sizes.
        """
        return (self.static_size[0] / self.dynamic_size[0], self.static_size[1] / self.dynamic_size[1])

    def draw(self, surface, position):
        """
        Draws a surface, into the dynamic texture.
        """
        flipped_y = self.context.window.internal_size[1] - position[1] - surface.get_height()
        self.dynamic_pass.draw(surface, (position[0], flipped_y))

    def dynamic_follow(self, position):
        self.dynamic_pass.camera.position.x = self.camera.offset.x * self.scale[0] * self.dynamic_size[0]
        self.dynamic_pass.camera.position.y = -self.camera.offset.y * self.scale[1] * self.dynamic_size[1]
        self.camera.offset.x = position[0] - 0.5 / self.scale[0]
        self.camera.offset.y = position[1] - 0.5 / self.scale[1]

    def set_scale(self):
        """
        Set the uniforms relative to the texture scales.
        """
        # the static texture takes covers all the UV space
        self.static_pass.set_uniform("tex_scale", (1.0, 1.0))
        # dynamic texture need to be rescaled
        self.dynamic_pass.set_uniform("tex_scale", self.scale)

    def set_offset(self):
        """
        Set the uniforms relative to the texture offsets.
        """
        # again, the static texture is the reference, it doesn't need to be repositioned
        self.static_pass.set_uniform("tex_offset", (0, 0))
        # the dynamic texture, yes
        self.dynamic_pass.set_uniform("tex_offset", (
            self.camera.offset.x, 
            self.camera.offset.y 
        ))
      
    def set_uniforms(self):
        for _pass in (self.static_pass, self.dynamic_pass):
            _pass.set_uniform("camera_x", self.camera.position.x)
            _pass.set_uniform("camera_y", self.camera.position.y)
            _pass.set_uniform("camera_z", self.camera.position.z)    
            _pass.set_uniform("camera_angle", self.camera.rotation)   
            _pass.set_uniform("horizon_height", self.camera.horizon_height)
            _pass.set_uniform("time", self.context.timer)
        self.set_offset()
        self.set_scale()
       
    def render(self):
        if self.context.scenes.current_scene in self.scenes:
            self.set_uniforms()
            # we force the static viewport to fit the screen, because the static texture is huge in size
            self.static_pass.set_viewport(0, 0, *self.context.window.internal_size)
            self.static_pass.render()
            self.dynamic_pass.render()