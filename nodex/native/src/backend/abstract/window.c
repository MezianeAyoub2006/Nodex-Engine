#include <stdio.h>
#include <stdlib.h>
#include "nodex/backend/abstract/window.h"
#include "nodex/macros/misc.h"

static NxWindow internalWindow;
static const NxWindowDriver* internalWindowDriver = NULL;

const NxWindow* Nx_WindowGet(void) {
    return &internalWindow;
}

void Nx_WindowInit(const NxWindowDriver* driver, NxWindow window) {
    if (!driver) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Window driver is NULL");
        return;
    }
    if (!driver->init) {
        Nx_SetStatus(NX_ERR_INVALID_DRIVER_INIT, "Window driver init function is NULL");
        return;
    }
    internalWindowDriver = driver;
    internalWindow = window;
    internalWindowDriver->init(&internalWindow);
}

void Nx_WindowSetVirtualSize(int virtualWidth, int virtualHeight) {
    NX_CHECK_DRIVER(internalWindowDriver, );
    NX_CHECK_FEATURE(internalWindowDriver->setVirtualSize, );
    if (virtualWidth <= 0 || virtualHeight <= 0) {
        Nx_SetStatus(NX_ERR_INVALID_ARGS, "Invalid virtual size");
        return;
    }
    internalWindow.virtualWidth = virtualWidth;
    internalWindow.virtualHeight = virtualHeight;
    internalWindowDriver->setVirtualSize(&internalWindow);
}

void Nx_WindowSetScale(float scale_X, float scale_Y) {
    NX_CHECK_DRIVER(internalWindowDriver, );
    NX_CHECK_FEATURE(internalWindowDriver->setScale, );
    if (scale_X <= 0 || scale_Y <= 0) {
        Nx_SetStatus(NX_ERR_INVALID_ARGS, "Invalid scale");
        return;
    }
    internalWindow.scale_X = scale_X;
    internalWindow.scale_Y = scale_Y;
    internalWindowDriver->setScale(&internalWindow);
}

void Nx_WindowSetTitle(const char* title) {
    NX_CHECK_DRIVER(internalWindowDriver, );
    NX_CHECK_FEATURE(internalWindowDriver->setTitle, );
    internalWindow.title = title;
    internalWindowDriver->setTitle(&internalWindow);
}

void Nx_WindowToggleFullscreen(void) {
    NX_CHECK_DRIVER(internalWindowDriver, );
    NX_CHECK_FEATURE(internalWindowDriver->toggleFullscreen, );
    internalWindow.fullscreen = !internalWindow.fullscreen;
    internalWindowDriver->toggleFullscreen(&internalWindow);
}

bool Nx_WindowShoudClose(void) {
    NX_DRIVER_DISPATCH(internalWindowDriver, shouldClose, false);
}
