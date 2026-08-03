#include <stdio.h>

#include "nodex/bridge/interface/interface.h"
#include "nodex/status/status.h"
#include "nodex/drivers/drivers.h"
#include "nodex/colors.h"

NxInterface interface; 

NxInterface* Nx_Interface_Get(void) {
    return &interface; 
}

void Nx_Interface_Init(void) {
    interface.status = NxInterface_Status_Get();  
    interface.should_close = false; 
    interface.rendering_queue = Nx_RenderingQueue_Get();
    interface.time.interval = 0.2f; 
}

static float interval_timer = 0.0f; 
static int frames = 0; 

static void Update_Time() {
    interface.time.dt = Nx_Get_Dt(); 
    interval_timer += interface.time.dt; 
    if (interval_timer >= interface.time.interval) {
        interface.time.fps = frames / interface.time.interval; 
        interval_timer -= interface.time.interval;  
        frames = 0; 
    }
    interface.time.timer += interface.time.dt; 
    frames++; 
}

void Nx_Interface_Update(void) {
    interface.should_close = Nx_Window_ShouldClose();
    Update_Time();  
    Nx_Renderer_Clear(NX_COLOR_BLACK);
    Nx_RenderingQueue_Update(); 
}  
