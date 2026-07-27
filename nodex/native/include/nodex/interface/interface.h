#ifndef INTERFACE_H
#define INTERFACE_H 

#include <stdbool.h>
#include "nodex/interface/queues/draw.h"
#include "nodex/interface/keyboard.h"
#include "nodex/status/status.h"  

typedef struct {
    bool shouldClose;   
    int fps; 
    float dt;  
    NxDrawQueue drawQueue;  
    NxDrawQueueFast drawQueueFast; 
    NxKeyboardState keyboardState; 
    NxStatus lastStatus;   
} NxInterface;

NxInterface* Nx_GetInterface(void);
void Nx_Update(void);

#endif 