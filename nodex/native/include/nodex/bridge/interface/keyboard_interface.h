#pragma once  

#include <stdbool.h>
#include <stdint.h>
#include "nodex/key.h"  

typedef struct {
    NxKey requested_keys[256]; 
    bool pressed_keys[256]; 
    bool active_keys[256]; 
    bool released_keys[256];
    uint32_t count; 
} NxInterface_Keyboard;


NxInterface_Keyboard* Nx_Interface_Keyboard_Get(void); 
void Nx_Interface_Keyboard_Update(void);
