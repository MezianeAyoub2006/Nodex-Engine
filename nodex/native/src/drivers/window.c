#include <stdio.h>
#include <stdint.h>

#include "nodex/drivers/window.h"
#include "nodex/status/status.h"
#include "macros.h" 
#include "nodex/macros.h"

static const NxWindowDriver* static_driver = NULL;
static NxWindow window; 

const NxWindow* Nx_Window_Get(void) { 
    return &window; 
} 

void Nx_Window_Init(const NxWindowDriver* driver, NxWindow window_template) {
    NX_DRIVER_CHECK(driver, static_driver, NX_DRIVER_WINDOW, NxWindowDriver*, "Window"); 
    static_driver = driver; 
    window = window_template;  
    NX_ERROR_IF(!window.caption, NX_ERR_ARGS, 
        "(window.caption): Expected a valid char*, (got NULL).", 
        return);
    NX_ERROR_IF(window.target_fps <= 0, NX_ERR_ARGS,
        "(window.target_fps): Expected a positive int, (got <= 0).",  
        return); 
    NX_REQUIRE_POSITIVE_VEC2(window.virtual_size, 
        "(window.virtual_size): "); 
    NX_REQUIRE_POSITIVE_VEC2(window.scale, 
        "(window.scale): ");  
    FULL_DISPATCH_VOID(static_driver, "Window", init, 
        &window); 
}

void Nx_Window_SetVirtualSize(NxVec2 virtual_size) {
    NX_REQUIRE_POSITIVE_VEC2(virtual_size, 
        "(virtual_size): "); 
    window.virtual_size = virtual_size; 
    FULL_DISPATCH_VOID(static_driver, "Window", set_virtual_size, 
        &window);  
}

void Nx_Window_SetScale(NxVec2 scale) {
    NX_REQUIRE_POSITIVE_VEC2(scale, 
        "(scale): ");  
    window.scale = scale; 
    FULL_DISPATCH_VOID(static_driver, "Window", set_scale, 
        &window);
}

void Nx_Window_SetTargetFps(int target_fps) {
    NX_ERROR_IF(target_fps <= 0, NX_ERR_ARGS,
        "(target_fps): Expected a positive int, (got <= 0).",  
        return); 
    window.target_fps = target_fps; 
    FULL_DISPATCH_VOID(static_driver, "Window", set_target_fps, 
        &window);
}  

void Nx_Window_SetCaption(const char* caption) {
    NX_ERROR_IF(!caption, NX_ERR_ARGS, 
        "(caption): Expected a valid char*, (got NULL).", 
        return);
    window.caption = caption; 
    FULL_DISPATCH_VOID(static_driver, "Window", set_caption, 
        &window);
}

void Nx_ToggleFullscreen(void) {
    FULL_DISPATCH_VOID(static_driver, "Window", toggle_fullscreen,
        &window);
}

bool Nx_Window_ShouldClose(void) {
    FULL_DISPATCH(static_driver, "Window", should_close, false, 
        &window); 
}