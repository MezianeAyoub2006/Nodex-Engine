#include "nodex/backend/abstract/backend.h"
#include "nodex/backend/raylib/raylib_renderer.h"
#include "nodex/backend/raylib/raylib_texture.h"
#include "nodex/backend/raylib/raylib_window.h"

NxBackend backendTable[N_BACKENDS];

void Nx_RegisterBackends(void) {
    backendTable[NX_BACKEND_RAYLIB] = (NxBackend){
        .windowDriver = Nx_GetRaylibWindowDriver(),
        .textureDriver = Nx_GetRaylibTextureDriver(),
        .rendererDriver = Nx_GetRaylibRendererDriver()
    };
}

NxStatus Nx_Init(
    NxBackend backend,
    int virtualWidth, 
    int virtualHeight,
    float scale_X,
    float scale_Y, 
    bool vsync, 
    const char* title
) {
    NxStatus status;

    status = Nx_WindowInit(backend.windowDriver, (NxWindow){
        .fullscreen    = false, 
        .scale_X       = scale_X,
        .scale_Y       = scale_Y,
        .virtualWidth  = virtualWidth, 
        .virtualHeight = virtualHeight, 
        .title         = title, 
        .vsync         = vsync,
    }); 
    if (status != NX_OKAY)
        return status;

    status = Nx_TextureInit(backend.textureDriver);
    if (status != NX_OKAY)
        return status;

    status = Nx_RendererInit(backend.rendererDriver); 
    if (status != NX_OKAY)
        return status;

    return NX_OKAY; 
}