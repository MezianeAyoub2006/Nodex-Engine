#include "nodex/interface/interface.h" 
#include "nodex.h"

NxInterface interface; 

NxInterface* Nx_GetInterface(void) {
    return &interface;
}

static void FillKeyboardState(void) {
    for (int i = 0; i < NX_KEY_NUMBER; i++)  {
        interface.keyboardState.active[i] = Nx_KeyActive(i); 
        interface.keyboardState.pressed[i] = Nx_KeyPressed(i); 
        interface.keyboardState.released[i] = Nx_KeyReleased(i); 
    }   
}

void Nx_Update(void) {
    interface.fps = Nx_GetFps(); 
    interface.dt = Nx_GetDt();
    interface.shouldClose = Nx_WindowShoudClose();
    interface.lastStatus = Nx_GetStatus(); 
    //FillKeyboardState(); 
    Nx_RendererBeginFrame(); 
    Nx_RendererClear((NxColor){.r = 0, .g = 0, .b = 0, .a = 0}); 
    for (int i = 0; i < interface.drawQueue.ptr; i++) {
        NxDrawTask task = interface.drawQueue.drawTasks[i]; 
        Nx_RendererDraw(
            task.texture,
            task.source,
            task.dest, 
            task.origin,
            task.rotation,
            task.tint 
        ); 
    }
    interface.drawQueue.ptr = 0; 
    for (int i = 0; i < interface.drawQueueFast.ptr; i++) {
        NxDrawTaskFast task = interface.drawQueueFast.drawTasks[i]; 
        Nx_RendererDrawFast(
            task.texture, 
            task.dest,
            task.tint 
        ); 
    }
    interface.drawQueueFast.ptr = 0; 
    Nx_RendererEndFrame(); 
    
}


