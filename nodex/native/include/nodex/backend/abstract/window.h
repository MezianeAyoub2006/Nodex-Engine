#ifndef WINDOW_H
#define WINDOW_H

#include "stdbool.h"
#include "nodex/status/status.h"

typedef struct {
    int virtualWidth; int virtualHeight;
    float scale_X; float scale_Y;
    bool fullscreen; bool vsync;
    const char* title;
} NxWindow;

typedef struct {
    void (*init)(NxWindow*);
    void (*setVirtualSize)(NxWindow*);
    void (*setScale)(NxWindow*);
    void (*setTitle)(NxWindow*);
    void (*toggleFullscreen)(NxWindow*);
    bool (*shouldClose)(void);
} NxWindowDriver;
 
const NxWindow* Nx_WindowGet(void);
void Nx_WindowInit(const NxWindowDriver* driver, NxWindow window);
void Nx_WindowSetVirtualSize(int virtualWidth, int virtualHeight);
void Nx_WindowSetScale(float scale_X, float scale_Y);
void Nx_WindowSetTitle(const char* title);
void Nx_WindowToggleFullscreen(void);
bool Nx_WindowShoudClose(void);

#endif