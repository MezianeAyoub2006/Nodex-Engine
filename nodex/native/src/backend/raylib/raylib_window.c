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

static void Raylib_WindowInit(NxWindow* window) {
    fflush(stdout);
    SetTraceLogLevel(LOG_NONE);
    SetConfigFlags(FLAG_WINDOW_HIDDEN);
    int rX, rY;
    get_real_size(window, &rX, &rY);
    NX_CHECK_NEGSIZE(rX, rY, );
    if (!window->title) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Window title is NULL");
        return;
    }
    InitWindow(rX, rY, window->title);
    BeginDrawing();
    ClearBackground(BLACK);
    EndDrawing();
    ClearWindowState(FLAG_WINDOW_HIDDEN);
}

static void Raylib_Rescale(NxWindow* window) {
    int rX, rY;
    get_real_size(window, &rX, &rY);
    NX_CHECK_NEGSIZE(rX, rY, );
    SetWindowSize(rX, rY);
}

static void Raylib_SetTitle(NxWindow* window) {
    if (!window->title) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Window title is NULL");
        return;
    }
    SetWindowTitle(window->title);
}

static void Raylib_ToggleFullscreen(NxWindow* window) {
    ToggleFullscreen();
}

static bool Raylib_ShouldClose() {
    return WindowShouldClose();
}

static const NxWindowDriver raylibDriver = {
    .init = &Raylib_WindowInit,
    .setScale = &Raylib_Rescale,
    .setVirtualSize = &Raylib_Rescale,
    .toggleFullscreen = &Raylib_ToggleFullscreen,
    .setTitle = &Raylib_SetTitle,
    .shouldClose = &Raylib_ShouldClose
};

const NxWindowDriver* Nx_GetRaylibWindowDriver(void) {
    return &raylibDriver;
}