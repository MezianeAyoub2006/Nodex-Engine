from .scene import Scene
import nodex
import pygame
import math

from .transition import Transition

class SceneManager:
    def __init__(self, context: "nodex.Context"):
        self.context = context
        self.persistant = Scene(self.context)
        self.scenes = {"main": Scene(self.context)}
        self.current_scene = "main"
        self._transition = Transition(self.context)

    def transition(self, scene, duration, effect = "circle", callback=lambda: None, callback_settings=()):
        self._transition.start(scene, duration, effect, callback, callback_settings)

    def switch(self, scene):
        self.current_scene = scene
        self.scenes[scene].load()

    def add_scene(self, name):
        self.scenes[name] = Scene(self.context)

    def update(self):
        self.scenes[self.current_scene].update()
        self.persistant.update()
        self.handle_transition()

    def handle_transition(self):
        if self._transition.done:
            return
        self._transition.update()
        if self._transition.halfway and self.current_scene != self._transition.scene:
            self.switch(self._transition.scene)
            self._transition.callback(*self._transition.callback_settings)

    @property
    def transition_done(self):
        return self._transition.done

    def __getitem__(self, scene):
        return self.scenes[scene]