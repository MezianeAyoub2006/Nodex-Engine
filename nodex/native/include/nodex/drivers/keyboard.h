#pragma once 

#include <stdbool.h>
#include "nodex/drivers/type.h"
#include "nodex/key.h" 

typedef struct NxKeyboardDriver {    
    NxDriverType type;
    bool (*get_pressed)(NxKey); 
    bool (*get_active)(NxKey); 
    bool (*get_released)(NxKey);  
} NxKeyboardDriver;   

void Nx_Keyboard_Init(const NxKeyboardDriver* driver); 
bool Nx_Keyboard_GetPressed(NxKey key); 
bool Nx_Keyboard_GetActive(NxKey key); 
bool Nx_Keyboard_GetReleased(NxKey key); 