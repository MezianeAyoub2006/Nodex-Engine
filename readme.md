# DISCLAIMER

This game doesn't use real 3D rendering, the 3D effect is a combination of 
- Spritestacking
- Billboarding
- Mode 7 (which is a fragment shader transformation)
Everything is contained into a quad, there is no 3D geometry, pygame is 
the core of the rendering. 

# INSTRUCTIONS

To run this game, with the same setup as me, you will need :
- pygame-ce 2.5.6
- Python 3.12.8 (will not work for some higher versions because of ModernGL)
- moderngl (pip install moderngl)
And if I'm not wrong, that's it (if it's missing modules just install the missing
ones).

# CONTROLS

F11 : toggle fullscreen

WASD : L for drift, SPACE for jump
ZQSD : L for drift, SPACE for jump (same)
ARROWS : X for drift, SPACE for jump  

When you die : 
SPACE to restart 
ESCAPTE to go back to the menu.