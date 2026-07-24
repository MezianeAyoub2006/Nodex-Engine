#include "nodex/backend/raylib/raylib_window.h"
#include "nodex/status/status.h"
#include "nodex/backend/abstract/window.h"
#include "nodex/misc.h"
#include "raylib/raylib.h"

static inline void get_real_size(const NxWindow* win, int* outW, int* outH) {
    *outW = (int)(win->virtualWidth * win->scale_X);
    *outH = (int)(win->virtualHeight * win->scale_Y);
}

NxStatus Nx_Raylib_WindowInit(NxWindow* window) {
    int rX, rY; 
    get_real_size(window, &rX, &rY); 
    NX_CHECK_NULLSIZE(rX, rY); 
    if (!window->title)
        return NX_ERR_NULLPTR; 
    InitWindow(rX, rY, window->title); 
    return NX_OKAY; 
}

NxStatus Nx_Raylib_WindowSetVirtualSize(NxWindow* window) {
    int rX, rY; 
    get_real_size(window, &rX, &rY); 
    NX_CHECK_NULLSIZE(rX, rY); 
    SetWindowSize(rX, rY); 
    return NX_OKAY; 
}

static const NxWindowDriver raylibDriver; 

const NxWindowDriver* Nx_GetRaylibWindowDriver(void) {
    return &raylibDriver; 
}
