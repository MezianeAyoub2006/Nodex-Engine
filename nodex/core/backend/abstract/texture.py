from typing import Type, Any
from abc import abstractmethod, ABC 

from ....math import Rectangle 

class AbstractTexture(ABC):

    """
    The texture is the main rendering ressource, it 
    represents 2D images with all the needed API to
    manipulate it, the CPU/GPU nature of it 
    is decided by the implementation. 
    """

    INJECTION_TYPE: Type[Any] = None

    """
    Controls whether the engine can inject data directly 
    into a texture, useful to implement direct wrappers.
    """

    """
    ####################
    ## STATIC METHODS ##
    #################### 
    """

    @staticmethod
    @abstractmethod 
    def inject(internal: Any) -> "AbstractTexture":

        """ 
        Creates a texture from another texture-like object. 
        This method is optional as long as AbstractTexture.INJECTION_TYPE is None. 

        Args:
            internal (Any): the texture-like object to inject into the returned texture.
        Returns:
            AbstractTexture: the texture where we injected internal. 
        """

        pass 

    @staticmethod
    @abstractmethod
    def blank(size: tuple[int, int]) -> "AbstractTexture":

        """
        Creates an blank texture (black and transparent).

        Args:
            size (tuple[int, int]): the size of the created texture.
        Returns:
            AbstractTexture: the returned blank texture.
        """

        pass

    """
    #################
    ## Texture API ##
    #################
    """

    @abstractmethod
    def __init__(self, path: str) -> None:

        """ 
        Loads a texture from an image file. 

        Args:
            path (str): the path of the image to load. 
        """

        pass

    @abstractmethod
    def fill(self, color: tuple[int, int, int, int]) -> None:

        """
        Fills the texture with the specified color. 

        Args:
            color (tuple[int, int, int, int]): the filling color.   
        """

        pass

    @abstractmethod
    def blit(self, texture: "AbstractTexture", position: tuple[int, int]) -> None:

        """
        Blits a texture into a specified position. 

        Args:
            texture (AbstractTexture): the texture to blit.
            position (position) : the topleft position, relatively to the current texture,
                of the blitted texture. 
        """

        pass

    @abstractmethod
    def view(self, region: Rectangle) -> "AbstractTexture":

        """
        Returns a view of the texture, which is a region of it, 
        sharing same pixels memory. 

        Args:
            region (Rectangle): the rectangle representing this region.
        Returns:
            AbstractTexture: the view of the texture. 
        """

        pass

    @abstractmethod
    def copy(self, region: Rectangle = None) -> "AbstractTexture":

        """
        Returns a copied region of the texture.

        Args:
            region (Rectangle): the rectangle representing this region.
        Returns:
            AbstractTexture: the copied region, as a new texture. 
        """

        pass

    @abstractmethod
    def free(self) -> None:
        """
        Frees the texture.
        """
        pass

    """
    #######################
    ## Getters / Setters ##
    #######################
    """

    @property
    @abstractmethod
    def size(self) -> tuple[int, int]:

        """
        Returns the size of the texture.

        Returns: 
            tuple[int, int]: the size of the texture
        """

        pass


        