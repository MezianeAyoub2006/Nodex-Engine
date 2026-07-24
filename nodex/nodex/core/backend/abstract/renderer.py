from abc import abstractmethod, ABC 

from ....math import Rectangle 

from .window import AbstractWindow
from .shader import AbstractShader
from .texture import AbstractTexture

class AbstractRenderer(ABC):

    """
    The renderer is the orchestrator of every rendering 
    functionalities. 
    """

    GPU_BACK: bool 

    """
    Controls weather the Backend is GPU oriented, this helps
    the engine knowing if things like shaders, post processing, etc.
    are implemented. 
    """

    """
    ##################
    ## Renderer API ##
    ##################
    """
    
    @abstractmethod
    def __init__(self, window: AbstractWindow):

        """
        Initialize a renderer. 

        Args:
            window (AbstractWindow): window to link to the renderer.  
        """

        pass

    # drawing

    @abstractmethod
    def draw_texture(self,  
            texture: AbstractTexture, 
            position: tuple[int, int],
            rotation: float = 0.0, 
            scale: tuple[int, int] = None,
            flip: tuple[bool, bool] = (False, False),
            tint: tuple[int, int, int, int] = (1.0, 1.0, 1.0, 1.0),
            shader: AbstractShader = None
        ) -> None:

        """
        Draws a texture.
        
        Args:
            texture (AbstractTexture): the texture to draw.
            position (tuple[int, int]): the (x, y) rendering position (the texture is centered to it).
            rotation (float): the rotation (in radiants) of the rendered texture.
            scale (tuple[int, int]): the scaling coeficients of the rendererd texture, in both dimentions.
            flip (tuple[bool, bool]): flip[0] controls if we flip the texture on the x-axis, same 
                for flip[1] on the y-axis.
            tint: (tuple[int, int, int, int]): the tint of the rendered texture, the final color is (tint.r * texture.r, ...).
            shader (AbstractShader): the shader to apply to render the texture. 
        """

        pass 

    @abstractmethod
    def draw_rectangle(self, 
            rectangle: Rectangle, 
            color: tuple[int, int, int, int], 
            shader: AbstractShader 
        ):

        """
        Draws a rectangle. 

        Args:
            rectangle (Rectangle): the rectangle to draw. 
            color: tuple[int, int, int, int]: the rendered rectangle color. 
            shader: the shader to apply to render the rectangle. 
        """
        pass 

    # engine hooks 

    @abstractmethod
    def before_frame(self):

        """
        Called before every rendering operations. 
        """

        pass

    @abstractmethod
    def after_frame(self):

        """
        Called after every rendering operations. 
        """

        pass

    # post processing 

    @abstractmethod
    def register_effect(self, effect_name: str, shader: AbstractShader) -> None:

        """
        Registers a post processing effect. 
        Args:
            effect_name (str): the name of the effect.
            shader (AbstractShader): the effect shader
        """

        pass

    @abstractmethod
    def activate_effect(self, effect_name: str) -> None:

        """
        Activate a post processing effect.
        Args:
            effect_name (str): the effect name. 
        """

        pass

    @abstractmethod
    def deactivate_effect(self, effect_name: str) -> None:

        """
        Deactivate a post processing effect.

        Args:
            effect_name (str): the effect name. 
        """

        pass

    @abstractmethod
    def is_effect_active(self, effect_name: str) -> bool:

        """
        Checks if a post processing effect is active.

        Args:
            effect_name (str): the effect name.
        Returns:
            bool: Weather the effect is active.
        """

        pass

    @abstractmethod
    def active_effects(self) -> list[str]:

        """
        Gives the list of every active post processing effects.

        Returns:
            list[str]: the list of every effect active, by name.
        """

        pass

    @abstractmethod
    def clear_effects(self) -> None:
        """
        Deactivate every post processing effect.
        """
        pass

    @abstractmethod
    def set_effect_uniform(self, effect_name: str, uniform: str, value) -> None:
        pass

    @abstractmethod
    def fill(self, color: tuple[int, int, int]) -> None:
        pass

    @abstractmethod 
    def release(self) -> None:
        pass
