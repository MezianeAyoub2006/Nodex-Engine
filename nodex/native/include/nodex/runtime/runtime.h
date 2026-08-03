#pragma once

#include "nodex/types/types.h"
#include "nodex/drivers/drivers.h"

void Nx_Init(
    NxVec2 virtual_size, 
    NxVec2 scale, 
    int flags, 
    int target_fps, 
    const char* caption,
    const NxWindowDriver* window_driver,
    const NxRendererDriver* renderer_driver,  
    const NxTextureDriver* texture_driver,
    float (*get_dt)(void)
);

void Nx_Update(void); 



