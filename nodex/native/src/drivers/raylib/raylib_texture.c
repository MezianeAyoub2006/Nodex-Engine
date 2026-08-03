#include <stdio.h>
#include <stdlib.h>

#include "raylib/raylib.h"
#include "nodex/drivers/texture.h" 
#include "nodex/status/status.h" 
#include "../macros.h"

NxTexture* Raylib_Texture_Load(const char* path) {
    Texture2D* raylib_texture = malloc(sizeof(*raylib_texture));

    NX_ERROR_IF(!raylib_texture, NX_ERR_OUT_OF_MEMORY, 
        "Raylib Texture2D memory allocation failed.", 
        return NULL);

    *raylib_texture = LoadTexture(path);

    NX_ERROR_IF(raylib_texture->id == 0, NX_ERR, 
        "Failed to load texture file.", 
        free(raylib_texture); 
        return NULL);
    
    NxTexture* texture = malloc(sizeof(*texture)); 

    NX_ERROR_IF(!texture, NX_ERR_OUT_OF_MEMORY, 
        "NxTexture memory allocation failed.", 
        UnloadTexture(*raylib_texture); 
        free(raylib_texture);        
        return NULL); 

    texture->raw = raylib_texture;  
    texture->size = (NxVec2){
        .x = (float)raylib_texture->width,
        .y = (float)raylib_texture->height
    }; 

    return texture; 
}   

void Raylib_Texture_Unload(NxTexture* texture) {
    UnloadTexture(*(Texture2D*)(texture->raw)); 
    free(texture->raw); 
    free(texture);
}

static NxTextureDriver static_driver = {
    .type = NX_DRIVER_TEXTURE,
    .load = &Raylib_Texture_Load,
    .unload = &Raylib_Texture_Unload   
}; 

const NxTextureDriver* Raylib_TextureDriver(void) {
    return &static_driver; 
}
