#include <stdlib.h>
#include "raylib/raylib.h"
#include "nodex/backend/raylib/raylib_texture.h"

static NxTextureFormat RaylibFormatToNodex(int raylibFormat) {
    switch (raylibFormat) {
        case PIXELFORMAT_UNCOMPRESSED_GRAYSCALE: 
            return NX_FORMAT_R8;
        case PIXELFORMAT_UNCOMPRESSED_R8G8B8:    
            return NX_FORMAT_R8G8B8;
        case PIXELFORMAT_UNCOMPRESSED_R8G8B8A8:  
            return NX_FORMAT_R8G8B8A8;
        default:                                 
            return NX_FORMAT_R8G8B8A8; 
    }
}

static NxStatus Raylib_TextureLoad(NxTexture* out, const char* path) {
    if (!out || !path) 
        return NX_ERR_NULLPTR;
    Texture2D* tex = malloc(sizeof(Texture2D));
    if (!tex) 
        return NX_ERR_OUT_OF_MEMORY;
    *tex = LoadTexture(path); 
    if (tex->id == 0) {
        free(tex); 
        return NX_ERR_INVALID_ARGS; 
    }
    out->prop = (NxTextureProp){
        .filter = NX_FILTER_POINT, 
        .wrap = NX_WRAP_CLAMP, 
        .pixelFormat = RaylibFormatToNodex(tex->format)
    }; 
    out->width = tex->width; 
    out->height = tex->height;
    out->raw = tex; 

    return NX_OKAY; 
}

static NxStatus Raylib_TextureUnload(NxTexture* out) {
    if (!out) 
        return NX_ERR_NULLPTR; 
    if (!out->raw) 
        return NX_ERR_NULLPTR; 
    UnloadTexture(*(Texture2D*)(out->raw));
    free(out->raw); 
    out->raw = NULL; 
    return NX_OKAY; 
}

static const NxTextureDriver raylibDriver = {
    .load = &Raylib_TextureLoad,
    .unload = &Raylib_TextureUnload, 
    .loadRaw = NULL,                  
    .setFilter = NULL,                
    .setWrap = NULL                   
};

const NxTextureDriver* Nx_GetRaylibTextureDriver(void) {
    return &raylibDriver; 
}
