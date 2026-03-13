from enum import Enum, auto
import nodex

class Material(Enum):
    WATER = auto()
    ICE = auto()
    GRASS = auto() 
    DEFAULT = auto()

MATERIALS_TABLE = {
    nodex.Color.RED : Material.ICE,
    nodex.Color.BLUE : Material.WATER,
    nodex.Color.GREEN : Material.GRASS
}

def material_under(context: "nodex.Context", position):
    w, h = context.globals["materials_map_size"]
    x = int(position.x * w)
    y = int((1.0 - position.y) * h)
    if x > 1024 or x < 0 or y > 1024 or y < 0:
        return Material.WATER
    try:
        color = tuple(context.globals["materials_map"][x][y]) 
        return MATERIALS_TABLE.get(color, Material.WATER)
    except:
        return Material.WATER
  