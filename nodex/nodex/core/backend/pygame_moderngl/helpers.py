import numpy as np  
from pathlib import Path

def make_quad(x1, y1, x2, y2):
    return np.array([
        x1, y1,  0.0, 1.0,
        x2, y1,  1.0, 1.0,
        x1, y2,  0.0, 0.0,
        x2, y1,  1.0, 1.0,
        x2, y2,  1.0, 0.0,
        x1, y2,  0.0, 0.0,
    ], dtype='f4')

CURRENT_DIR = Path(__file__).parent

def load_shader(filename: str) -> str:
    return (CURRENT_DIR / filename).read_text()

