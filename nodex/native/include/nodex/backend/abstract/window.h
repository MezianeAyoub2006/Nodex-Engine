#ifndef WINDOW_H
#define WINDOW_H

#include "stdbool.h"
#include "nodex/status/status.h"

#define NX_CHECK_DRIVER(driver) \
    do { \
        if (!(driver)) \
            return NX_ERR_DRIVER_NULL; \
    } while (0) 
 
#define NX_CHECK_FEATURE(func_ptr) \
    do { \
        if (!(func_ptr)) \
            return NX_WARN_FEATURE_NOT_SUPPORTED; \
    } while (0)

typedef struct { 
    int virtualWidth; 
    int virtualHeight; 
    float scale_X;
    float scale_Y; 
    bool fullscreen;
    bool vsync; 
    const char* title; 
} NxWindow;

typedef struct {
    NxStatus (*init)(NxWindow*);
    NxStatus (*setVirtualSize)(NxWindow*);
    NxStatus (*setScale)(NxWindow*);
    NxStatus (*setTitle)(NxWindow*);
    NxStatus (*toggleFullscreen)(NxWindow*);
} NxWindowDriver;

const NxWindow* Nx_WindowGet(void); 
NxStatus Nx_WindowInit(const NxWindowDriver* driver, NxWindow window); 
NxStatus Nx_WindowSetVirtualSize(int virtualWidth, int virtualHeight); 
NxStatus Nx_WindowSetScale(float scale_X, float scale_Y); 
NxStatus Nx_WindowSetTitle(const char* title);
NxStatus Nx_WindowToggleFullscreen(void);

#endif