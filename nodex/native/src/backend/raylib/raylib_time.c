#include <stdio.h>

#include "raylib/raylib.h"
#include "nodex/backend/abstract/time.h"

static void Raylib_SetTargetFps(int fps) {
    printf("ON A SET A %d\n", fps);
    SetTargetFPS(fps);
}

static const NxTimeDriver raylibTimeDriver = {
    .getDt = &GetFrameTime,
    .getFps = &GetFPS,
    .setTargetFps = &Raylib_SetTargetFps
};

const NxTimeDriver* Nx_GetRaylibTimeDriver(void) {
    return &raylibTimeDriver;
}