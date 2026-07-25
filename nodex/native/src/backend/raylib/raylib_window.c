#include "nodex/backend/raylib/raylib_window.h"
#include "nodex/status/status.h"
#include "nodex/backend/abstract/window.h"
#include "nodex/macros/misc.h"
#include "raylib/raylib.h"
#include <stdio.h>

static inline void get_real_size(const NxWindow* win, int* outW, int* outH) {
    *outW = (int)(win->virtualWidth * win->scale_X);
    *outH = (int)(win->virtualHeight * win->scale_Y);
}

static NxStatus Raylib_WindowInit(NxWindow* window) {
    fflush(stdout);
    SetTraceLogLevel(LOG_NONE);
    SetConfigFlags(FLAG_WINDOW_HIDDEN); 
    int rX, rY; 
    get_real_size(window, &rX, &rY); 
    NX_CHECK_NEGSIZE(rX, rY); 
    if (!window->title)
        return NX_ERR_NULLPTR; 
    InitWindow(rX, rY, window->title); 
    BeginDrawing(); 
    ClearBackground(BLACK); 
    EndDrawing(); 
    ClearWindowState(FLAG_WINDOW_HIDDEN);
    return NX_OKAY; 
}

static NxStatus Raylib_Rescale(NxWindow* window) {
    int rX, rY; 
    get_real_size(window, &rX, &rY); 
    NX_CHECK_NEGSIZE(rX, rY); 
    SetWindowSize(rX, rY); 
    return NX_OKAY; 
}

static NxStatus Raylib_SetTitle(NxWindow* window) {
    if (!window->title)
        return NX_ERR_NULLPTR; 
    SetWindowTitle(window->title); 
    return NX_OKAY;
}; 
static NxStatus Raylib_ToggleFullscreen(NxWindow* window) {
    ToggleFullscreen();
    return NX_OKAY; 
} 

static const NxWindowDriver raylibDriver = {
    .init = &Raylib_WindowInit,
    .setScale = &Raylib_Rescale,
    .setVirtualSize = &Raylib_Rescale, 
    .toggleFullscreen = &Raylib_ToggleFullscreen, 
    .setTitle = &Raylib_SetTitle 
}; 

const NxWindowDriver* Nx_GetRaylibWindowDriver(void) {
    return &raylibDriver; 
}
