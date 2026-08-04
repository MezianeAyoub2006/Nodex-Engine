#include <stdio.h>
#include "nodex/runtime/runtime.h"

#include "nodex/drivers/drivers.h"
#include "nodex/bridge/interface/interface.h"
#include "nodex/colors.h"
#include "flags.h"

void Nx_Init(
    NxVec2 virtual_size, 
    NxVec2 scale, 
    int flags, 
    int target_fps, 
    const char* caption,
    const NxWindowDriver* window_driver,
    const NxRendererDriver* renderer_driver,  
    const NxTextureDriver* texture_driver,
    const NxKeyboardDriver* keyboard_driver, 
    float (*get_dt)(void)
) {
    #if defined(NX_DEBUG) && defined(NX_PERF)
        printf("Hello WAAA\n");
        Nx_ThrowError( 
            NX_ERR_PREPROCESS, 
            "[ Engine ]", 
            "Cannot define NX_DEBUG and NX_PERF at the same time."
        );
    #endif
    NX_CHECK();   
    Nx_Window_Init(
        window_driver, 
        (NxWindow) {
            .virtual_size = virtual_size,
            .scale = scale,
            .target_fps = target_fps,
            .flags = flags, 
            .caption = caption,
            .fullscreen = false,
            .stretch = false
        } 
    ); 
    Nx_Renderer_Init(renderer_driver);
    Nx_Texture_Init(texture_driver);
    Nx_Keyboard_Init(keyboard_driver); 
    Nx_Dt_Init(get_dt);      
    Nx_Interface_Init();
}

void Nx_Update(void) {
    NxInterface* interface = Nx_Interface_Get();
    Nx_Interface_Keyboard_Update(); 
    Nx_Renderer_BeginFrame(); 
    Nx_Interface_Update();  
    Nx_Renderer_EndFrame(); 
} 




