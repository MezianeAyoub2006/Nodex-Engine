class ParallaxLayer:
    def __init__(self, context, image_name: str, speed: float = 20.0, vertical_coef: float = 10.0):
        self.context = context
        self.image_name = image_name
        self.speed = speed
        self.vertical_coef = vertical_coef

    def draw(self, cam):
        img = self.context.assets.get_image(self.image_name)
        img_w = img.get_width()
        w, _ = self.context.window.internal_size

        coef = 1.0 + max(0.0, -cam.position.z) * self.vertical_coef
        scroll = (cam.rotation * self.speed * coef) % img_w
        x = scroll - img_w

        self.context.renderer.draw("background", self.image_name, position=(x, 0))
        if x + img_w < w:
            self.context.renderer.draw("background", self.image_name, position=(x + img_w, 0))

class ParallaxObject:
    def __init__(
        self,
        context,
        image_name: str,
        base_x: float,
        y: float,
        speed: float = 20.0,
        cycle: int = None,
        auto_speed: float = 0.0,
        repeat: bool = True,
        world_size: int = 1024
    ):
        self.context = context
        self.image_name = image_name
        self.base_x = base_x
        self.y = y

        self.speed = speed
        self.cycle = cycle
        self.auto_speed = auto_speed
        self.repeat = repeat
        self.world_size = world_size

        self._offset = 0.0

    def _update_offset(self):
        self._offset += self.auto_speed * self.context.dt

        if self.repeat:
            img = self.context.assets.get_image(self.image_name)
            cycle = self.cycle or self.context.window.internal_size[0]
            self._offset %= (cycle + img.get_width())
        else:
            self._offset %= self.world_size

    def _compute_x(self, cam, img_w, viewport_w):
        rotation_offset = cam.rotation * self.speed
        if self.repeat:
            cycle = self.cycle or viewport_w
            x = (self.base_x + self._offset + rotation_offset) % (cycle + img_w) - img_w
        else:
            x = (self.base_x + self._offset + rotation_offset) % (self.world_size + img_w) - img_w

        return x

    def draw(self, cam, viewport):
        img = self.context.assets.get_image(self.image_name)
        img_w = img.get_width()
        viewport_w, _ = self.context.window.internal_size

        self._update_offset()
        x = self._compute_x(cam, img_w, viewport_w)

        self.context.renderer.draw(
            viewport,
            self.image_name,
            position=(x, self.y)
        )