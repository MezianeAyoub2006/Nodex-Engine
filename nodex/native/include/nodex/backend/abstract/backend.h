#ifndef BACKEND_H
#define BACKEND_H

#include "nodex/backend/abstract/renderer.h"
#include "nodex/backend/abstract/texture.h"
#include "nodex/backend/abstract/window.h"
#include "nodex/backend/abstract/keyboard.h"
#include "nodex/backend/abstract/time.h"

#define N_BACKENDS 1

typedef enum {
    NX_BACKEND_RAYLIB = 0
} NxBackends;

typedef struct {
    NxWindowDriver* windowDriver;
    NxTextureDriver* textureDriver;
    NxRendererDriver* rendererDriver;
    NxKeyboardDriver* keyboardDriver;
    NxTimeDriver* timeDriver;
} NxBackend;

NxBackend* Nx_GetBackendTable(void); 

void Nx_RegisterBackends(void);

void Nx_Init(
    NxBackend backend,
    int virtualWidth, int virtualHeight,
    float scale_X, float scale_Y,
    bool vsync, int targetFps,
    const char* title
);

#endif