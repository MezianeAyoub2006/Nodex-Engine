#include "raylib/raylib.h"
#include "nodex/drivers/ray/ray.h"

float Raylib_Get_Dt(void) {
    return GetFrameTime();
} 
