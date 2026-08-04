#include "nodex/bridge/interface/keyboard_interface.h"
#include "nodex/drivers/keyboard.h"

static NxInterface_Keyboard static_interface; 

NxInterface_Keyboard* Nx_Interface_Keyboard_Get(void) {
    return &static_interface;
}

void Nx_Interface_Keyboard_Update(void) {
    for (int i = 0; i < static_interface.count; i++) {
        NxKey requested_key = static_interface.requested_keys[i];  
        static_interface.pressed_keys[requested_key] = Nx_Keyboard_GetPressed(requested_key);
        static_interface.active_keys[requested_key] = Nx_Keyboard_GetActive(requested_key);
        static_interface.released_keys[requested_key] = Nx_Keyboard_GetReleased(requested_key);
    }
}