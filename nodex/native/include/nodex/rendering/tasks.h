#pragma once 

#include <stdint.h>
#include "nodex/drivers/texture.h"

typedef struct {
    NxTexture* texture;  
    float pos_x; 
    float pos_y; 
} NxTaskSimple;
 
typedef struct {
    NxTexture* texture;  
    float pos_x; 
    float pos_y; 
    float rotation;
    float scale; 
} NxTaskNormal;

typedef struct {
    NxTexture* texture;  
    float source_x; 
    float source_y; 
    float source_w; 
    float source_h; 
    float dest_x;
    float dest_y;
    float dest_w;
    float dest_h; 
    float origin_x; 
    float origin_y; 
    float rotation; 
    uint8_t tint_r; 
    uint8_t tint_g; 
    uint8_t tint_b; 
    uint8_t tint_a; 
} NxTaskFull;
