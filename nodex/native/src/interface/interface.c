#include "nodex/interface/interface.h" 
#include "nodex.h"

PyInterface interface; 

PyInterface* Nx_GetInterface(void) {
    return &interface;
}

/*
static void FillKeyboardState(void) {
    for (int i = 0; i < NX_KEY_NUMBER; i++)  {
        interface.keyboardState.active[i] = Nx_KeyActive(i); 
        interface.keyboardState.pressed[i] = Nx_KeyPressed(i); 
        interface.keyboardState.released[i] = Nx_KeyReleased(i); 
    }   
}
*/
void Nx_Update(void) {
    interface.read.time.fps = Nx_GetFps(); 
    interface.read.time.dt = Nx_GetDt();
    interface.read.flags.shouldClose = Nx_WindowShoudClose();
    interface.read.status.last = Nx_GetStatus(); 
    interface.read.status.message = Nx_GetStatusMessage(); 
    //FillKeyboardState(); 
    Nx_RendererBeginFrame(); 
    Nx_RendererClear((NxColor){.r = 0, .g = 0, .b = 0, .a = 0}); 
    for (int i = 0; i < interface.write.draw.full.ptr; i++) {
        PyDrawTaskFull task = interface.write.draw.full.tasks[i]; 
        Nx_RendererDraw(
            task.texture,
            task.source,
            task.dest, 
            task.origin,
            task.rotation,
            task.tint 
        ); 
    }
    interface.write.draw.full.ptr = 0; 
    for (int i = 0; i < interface.write.draw.fast.ptr; i++) {
        PyDrawTaskFast task = interface.write.draw.fast.tasks[i]; 
        Nx_RendererDrawFast(
            task.texture, 
            task.dest,
            task.tint 
        ); 
    }
    interface.write.draw.fast.ptr = 0; 
    Nx_RendererEndFrame(); 
}


