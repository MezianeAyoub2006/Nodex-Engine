#include <stdlib.h>

#include "raylib/raylib.h"
#include "nodex/drivers/ray/ray_window.h"
#include "nodex/status/status.h"
#include "../macros.h"
#include "nodex/system/platform.h"


#define WARN_TARGET_FPS                                                     \
Nx_ThrowWarning(                                                            \
    NX_WARN_TIMING,                                                         \
    NX_PRIORITY_MID,                                                        \
    "Vsync enabled with high target fps."                                   \
);

static void Raylib_Window_Rescale(NxWindow* window) {
    SetWindowSize(
        (int)(window->virtual_size.x * window->scale.x),
        (int)(window->virtual_size.y * window->scale.y)
    );
}

static int Raylib_Refresh_Rate(void) {
    return GetMonitorRefreshRate(GetCurrentMonitor());
}

static bool Get_Window_Vsync(NxWindow* window) {
    return (window->flags & NX_FLAG_VSYNC) != 0;
}

static void Raylib_Window_Center(void) {
    int monitor = GetCurrentMonitor();
    int mw = GetMonitorWidth(monitor);
    int mh = GetMonitorHeight(monitor);
    int ww = GetScreenWidth();
    int wh = GetScreenHeight();
    SetWindowPosition((mw - ww) / 2, (mh - wh) / 2);
}

static void Raylib_Window_Init(NxWindow* window) {
    SetTraceLogLevel(LOG_NONE);

    bool vsync = Get_Window_Vsync(window);

    if (vsync) SetConfigFlags(FLAG_VSYNC_HINT);
    SetConfigFlags(FLAG_WINDOW_HIDDEN);

    InitWindow(
        (int)(window->virtual_size.x * window->scale.x),
        (int)(window->virtual_size.y * window->scale.y),
        window->caption
    );


    if (vsync && (window->target_fps > Raylib_Refresh_Rate())) {
        WARN_TARGET_FPS;
    } else if (!vsync) {
        SetTargetFPS(window->target_fps);
    }

    Raylib_Window_Center();

    BeginDrawing();
    ClearBackground(BLACK);
    EndDrawing();
    
    ClearWindowState(FLAG_WINDOW_HIDDEN);
}

static bool Raylib_Window_ShouldClose(NxWindow* window) {
    return WindowShouldClose();
}

static void Raylib_Window_SetCaption(NxWindow* window) {
    SetWindowTitle(window->caption);
}

static void Raylib_Window_SetScale(NxWindow* window) {
    Raylib_Window_Rescale(window);
}

static void Raylib_Window_SetTargetFps(NxWindow* window) {
    bool vsync = Get_Window_Vsync(window);
    if (window->target_fps > Raylib_Refresh_Rate() && vsync)
        Nx_ThrowWarning(
            NX_WARN_TIMING,
            NX_PRIORITY_MID,
            "(VSYNC): FPS Will be limited to 60."
        );
    SetTargetFPS(window->target_fps);
}

static void Raylib_Window_SetVirtualSize(NxWindow* window) {
    Raylib_Window_Rescale(window);
}

static void Raylib_Window_ToggleFullscreen(NxWindow* window) {
    if (!IsWindowState(FLAG_WINDOW_UNDECORATED)) {
        int monitor = GetCurrentMonitor();
        int mw = GetMonitorWidth(monitor);
        int mh = GetMonitorHeight(monitor);
        SetWindowState(FLAG_WINDOW_UNDECORATED);
        SetWindowSize(mw, mh - 1);
        SetWindowPosition(0, 0);
    } else {
        ClearWindowState(FLAG_WINDOW_UNDECORATED);
        Raylib_Window_Rescale(window);
        int monitor = GetCurrentMonitor();
        int mw = GetMonitorWidth(monitor);
        int mh = GetMonitorHeight(monitor);
        int ww = (int)(window->virtual_size.x * window->scale.x);
        int wh = (int)(window->virtual_size.y * window->scale.y);
        SetWindowPosition((mw - ww) / 2, (mh - wh) / 2);
    }
}

static NxWindowDriver static_driver = {
    .type = NX_DRIVER_WINDOW,
    .init = &Raylib_Window_Init,
    .should_close = &Raylib_Window_ShouldClose,
    .set_caption = &Raylib_Window_SetCaption,
    .set_scale = &Raylib_Window_Rescale,
    .set_target_fps = &Raylib_Window_SetTargetFps,
    .set_virtual_size = &Raylib_Window_SetVirtualSize,
    .toggle_fullscreen = &Raylib_Window_ToggleFullscreen
};

const NxWindowDriver* Raylib_WindowDriver(void) {
    return &static_driver;
}