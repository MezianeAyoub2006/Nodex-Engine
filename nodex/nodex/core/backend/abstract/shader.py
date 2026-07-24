from typing import Any
from abc import abstractmethod, ABC 

from .texture import AbstractTexture

class AbstractShader(ABC):
    """
    The shader represents a GPU program centralizing 
    a compiled program, textures, and uniforms.
    """

    """
    ####################
    ## Static Methods ##
    #################### 
    """

    @staticmethod
    @abstractmethod  
    def passthrough_shader() -> "AbstractShader": 

        """
        Returns a shader that does nothing. 

        Returns:
            AbstractShader: the passthrough shader. 
        """
        pass 

    """
    ################
    ## Shader API ##
    ################
    """

    @abstractmethod
    def __init__(self, fragment_shader: str, vertex_shader: str):

        """
        Initialize a shader taking both fragment and vertex shader 
        programs. 

        Args:
            fragment_shader (str): the fragment shader program.
            vertex_shader (str): the vertex shader program. 
        """

        pass

    @abstractmethod
    def set_uniform(self, variable: str, value: Any) -> None:

        """
        Sets a GLSL uniform to a specified value.
        Args:
            variable (str): the GLSL uniform name. 
            value (Any): the value to put. 
        """

        pass

    @abstractmethod
    def set_texture(self, variable: str, texture: AbstractTexture) -> None:

        """ 
        Sets a GLSL sampler2D to a specified texture. 

        Args:
            variable (str): the GLSL sampler2D uniform name.
            value (AbstractTexture): the texture to put. 
        """

        pass

    @abstractmethod
    def free(self):

        """
        Frees the shader.
        """

        pass