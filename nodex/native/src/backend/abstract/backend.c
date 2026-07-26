#include <stdio.h>

#include "nodex/backend/abstract/backend.h"

#include "nodex/backend/raylib/raylib_renderer.h"
#include "nodex/backend/raylib/raylib_texture.h"
#include "nodex/backend/raylib/raylib_window.h"
#include "nodex/backend/raylib/raylib_keyboard.h"
#include "nodex/backend/raylib/raylib_time.h"
#include "nodex/backend/abstract/time.h"

static NxBackend backendTable[N_BACKENDS];

void Nx_RegisterBackends(void) {
    backendTable[NX_BACKEND_RAYLIB] = (NxBackend){
        .windowDriver = Nx_GetRaylibWindowDriver(),
        .textureDriver = Nx_GetRaylibTextureDriver(),
        .rendererDriver = Nx_GetRaylibRendererDriver(),
        .keyboardDriver = Nx_GetRaylibKeyboardDriver(),
        .timeDriver = Nx_GetRaylibTimeDriver()
    };
}

NxBackend* Nx_GetBackendTable(void) {
    return &backendTable;
}

void Nx_Init(
    NxBackend backend,
    int virtualWidth,
    int virtualHeight,
    float scale_X,
    float scale_Y,
    bool vsync,
    int targetFps,
    const char* title
) {
    Nx_WindowInit(backend.windowDriver, (NxWindow){
        .fullscreen = false,
        .scale_X = scale_X,
        .scale_Y = scale_Y,
        .virtualWidth = virtualWidth,
        .virtualHeight = virtualHeight,
        .title = title,
        .vsync = vsync,
    });
    if (Nx_GetStatus() != NX_OKAY)
        return;

    Nx_TextureInit(backend.textureDriver);
    printf("status1 %d", Nx_GetStatus());
    if (Nx_GetStatus() != NX_OKAY)
        return;

    Nx_RendererInit(backend.rendererDriver);
    printf("status2 %d", Nx_GetStatus());
    if (Nx_GetStatus() != NX_OKAY)
        return;

    Nx_KeyboardInit(backend.keyboardDriver);
    printf("status3 %d", Nx_GetStatus());
    if (Nx_GetStatus() != NX_OKAY)
        return;

    Nx_TimeInit(backend.timeDriver, (NxTime){.targetFps = targetFps});
    printf("status4 %d", Nx_GetStatus());
    if (Nx_GetStatus() != NX_OKAY)
        return;

    Nx_SetTargetFps(targetFps);
    printf("status5 %d", Nx_GetStatus());
    if (Nx_GetStatus() != NX_OKAY)
        return;
}