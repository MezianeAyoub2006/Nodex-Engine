#ifndef WINDOW_H
#define WINDOW_H

#include "stdbool.h"
#include "nodex/status/status.h"

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