from abc import abstractmethod, ABC 

class AbstractWindow(ABC):

    """ 
    Abstract definition of the window.
    """

    """
    ################
    ## Window API ##
    ################
    """

    @abstractmethod
    def __init__(self, virtual_size: tuple[int, int], scale: float, vsync: bool, caption: str):
    
        """
        Creates a new window.

        Args:
            virtual_size (tuple[int, int]): The virtual size of the window, everything will be rendered relative to this size.
            scale (float): The coefficient between the virtual size and the real size 
                of the window.
            vsync (bool): Controls if vsync is activated or not.
            caption (str): The caption of the window.
        """
        
        pass


    @abstractmethod
    def rescale(self, virtual_size: tuple[int, int] = None, scale: float = None) -> None:

        """        
        Rescales the window.

        Args:
            virtual_size (tuple[int, int]): the new virtual size.
            scale (float): the new scale.
        """
        
        pass

    @abstractmethod
    def toggle_fullscreen(self) -> None:

        """
        Toggles fullscreen. 
        """

        pass

    @abstractmethod
    def set_caption(self, caption: str) -> None:

        """
        Change the caption of the window.

        Args:
            caption (str): The new caption.
        """

        pass

    """
    #######################
    ## Getters / Setters ##
    ####################### 
    """

    @property
    @abstractmethod
    def virtual_size(self) -> tuple[float, float]:

        """
        Returns:
            tuple[float, float]: the virtual size of the window.
        """

        pass

    @property
    @abstractmethod
    def scale(self) -> float:

        """
        Returns:
            float: the scale of the window.
        """

        pass

    @property
    @abstractmethod
    def is_fullscreen(self) -> bool:

        """
        Returns:
            bool: false if the window is windowed, 
            true if the window is fullscreen.
        """

        pass


    @property
    @abstractmethod
    def caption(self) -> str:
        """
        Returns:
            str: the caption of the window.
        """
        pass

    """
    ###################################
    ## Non-abstract functionalities. ##
    ###################################
    """

    @property
    def size(self) -> tuple[int, int]:

        """
        Returns:
            tuple[int, int]: the real size of the window.
        """

        return (
            self.virtual_size[0] * self.scale,
            self.virtual_size[1] * self.scale
        )   