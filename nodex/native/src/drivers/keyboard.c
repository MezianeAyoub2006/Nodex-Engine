#include <stdlib.h>
#include "nodex/drivers/keyboard.h"
#include "macros.h" 
#include "nodex/macros.h"
#include "nodex/drivers/type.h"

static const NxKeyboardDriver* static_driver = NULL;

void Nx_Keyboard_Init(const NxKeyboardDriver* driver) {
    NX_DRIVER_CHECK(driver, static_driver, NX_DRIVER_KEYBOARD, NxKeyboardDriver*, "Keyboard"); 
    static_driver = driver; 
}  

bool Nx_Keyboard_GetPressed(NxKey key) {
    FULL_DISPATCH(static_driver, "Keyboard", get_pressed, false, 
        key); 
}

bool Nx_Keyboard_GetActive(NxKey key) {
    FULL_DISPATCH(static_driver, "Keyboard", get_active, false, 
        key); 
} 
bool Nx_Keyboard_GetReleased(NxKey key) {
    FULL_DISPATCH(static_driver, "Keyboard", get_released, false, 
        key); 
}