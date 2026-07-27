#ifndef INTERFACE_H
#define INTERFACE_H 

#include <stdbool.h>
#include "nodex/interface/queues/draw.h"
#include "nodex/interface/keyboard.h"

typedef struct {
    bool shouldClose;   
    int fps; 
    float dt;  
    NxDrawQueue drawQueue;  
    NxDrawQueueFast drawQueueFast; 
    NxKeyboardState keyboardState; 
    // inserer interface pour python ici
} NxInterface;

NxInterface* Nx_GetInterface(void);
void Nx_Update(void);

#endif 