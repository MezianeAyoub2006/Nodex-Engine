#ifndef INTERFACE_INPUT_H
#define INTERFACE_INPUT_H

#include "nodex/backend/abstract/keyboard.h"

typedef struct {
    bool active[NX_KEY_NUMBER]; 
    bool pressed[NX_KEY_NUMBER]; 
    bool released[NX_KEY_NUMBER]; 
} PyKeyboardRead; 

typedef struct {
    NxKey keys[NX_KEY_NUMBER]; 
    int ptr; 
} PyKeyboardRequested; 

#endif 