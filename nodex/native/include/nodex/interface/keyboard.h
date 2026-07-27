#ifndef INTERFACE_KEYBOARD_H
#define INTERFACE_KEYBOARD_H 

#include "nodex/backend/abstract/keyboard.h"  

typedef struct {
    bool active[NX_KEY_NUMBER]; 
    bool pressed[NX_KEY_NUMBER]; 
    bool released[NX_KEY_NUMBER]; 
} NxKeyboardState; 

#endif 