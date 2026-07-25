#ifndef BACKEND_H
#define BACKEND_H

#include "nodex/backend/abstract/renderer.h"
#include "nodex/backend/abstract/texture.h"
#include "nodex/backend/abstract/window.h" 

#define N_BACKENDS 1

typedef enum {
    NX_BACKEND_RAYLIB = 0 
} NxBackends; 

typedef struct {
    NxWindowDriver* windowDriver;
    NxTextureDriver* textureDriver; 
    NxRendererDriver* rendererDriver; 
} NxBackend; 

extern NxBackend backendTable[N_BACKENDS];

void Nx_RegisterBackends(void);

NxStatus Nx_Init(
    NxBackend backend,
    int virtualWidth, 
    int virtualHeight,
    float scale_X,
    float scale_Y, 
    bool vsync, 
    const char* title
);

#endif 
