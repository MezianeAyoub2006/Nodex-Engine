from ..exceptions import NativeException 
from ....core.exceptions import CoreException

class TextureException(NativeException):
    __module__ = "nodex"

class TexturePathException(TextureException):
    __module__ = "nodex"
    
class WindowException(CoreException): 
    __module__ = "nodex"
