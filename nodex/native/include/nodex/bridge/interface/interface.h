#pragma once 

#include <stdbool.h>
#include "nodex/status/status.h"
#include "nodex/drivers/window.h"
#include "nodex/rendering/rendering.h"
#include "nodex/bridge/interface/time.h"
#include "nodex/bridge/interface/keyboard_interface.h" 

typedef struct {
    bool should_close; 
    NxWindow* window;
    NxInterface_Status* status; 
    NxRenderingQueue* rendering_queue;
    NxInterface_Keyboard* keyboard; 
    NxInterface_Time time;  
} NxInterface; 

void Nx_Interface_Init(void); 
void Nx_Interface_Update(void);
NxInterface* Nx_Interface_Get(void); 

