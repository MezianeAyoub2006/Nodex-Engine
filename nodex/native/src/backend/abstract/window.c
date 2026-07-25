#include <stdio.h>
#include <stdlib.h>
#include "nodex/backend/abstract/window.h"
#include "nodex/macros/misc.h"

static NxWindow internalWindow; 
static const NxWindowDriver* internalWindowDriver = NULL; 

const NxWindow* Nx_WindowGet(void) {
    return &internalWindow; 
}

NxStatus Nx_WindowInit(const NxWindowDriver* driver, NxWindow window) {
    if (!driver) 
        return NX_ERR_NULLPTR;  
    if (!driver->init) 
        return NX_ERR_INVALID_DRIVER_INIT;  
    internalWindowDriver = driver; 
    internalWindow = window; 
    return internalWindowDriver->init(&internalWindow);
}


NxStatus Nx_WindowSetVirtualSize(int virtualWidth, int virtualHeight) {
    NX_CHECK_DRIVER(internalWindowDriver); 
    NX_CHECK_FEATURE(internalWindowDriver->setVirtualSize); 
    if (virtualWidth <= 0 || virtualHeight <= 0) 
        return NX_ERR_INVALID_ARGS; 
    internalWindow.virtualWidth = virtualWidth; 
    internalWindow.virtualHeight = virtualHeight; 
    return internalWindowDriver->setVirtualSize(&internalWindow);
}

NxStatus Nx_WindowSetScale(float scale_X, float scale_Y) {
    NX_CHECK_DRIVER(internalWindowDriver); 
    NX_CHECK_FEATURE(internalWindowDriver->setScale);
    if (scale_X <= 0 || scale_Y <= 0)
        return NX_ERR_INVALID_ARGS;  
    internalWindow.scale_X = scale_X; 
    internalWindow.scale_Y = scale_Y; 
    return internalWindowDriver->setScale(&internalWindow);
}

NxStatus Nx_WindowSetTitle(const char* title) {
    NX_CHECK_DRIVER(internalWindowDriver); 
    NX_CHECK_FEATURE(internalWindowDriver->setTitle); 
    internalWindow.title = title; 
    return internalWindowDriver->setTitle(&internalWindow); 
}

NxStatus Nx_WindowToggleFullscreen(void) {
    NX_CHECK_DRIVER(internalWindowDriver); 
    NX_CHECK_FEATURE(internalWindowDriver->toggleFullscreen); 
    internalWindow.fullscreen = !internalWindow.fullscreen; 
    return internalWindowDriver->toggleFullscreen(&internalWindow); 
}