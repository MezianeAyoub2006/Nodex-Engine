#include <stdlib.h>
#include "nodex/backend/abstract/keyboard.h"
#include "nodex/macros/misc.h"

static const NxKeyboardDriver* keyboardDriver = NULL;

void Nx_KeyboardInit(const NxKeyboardDriver* driver) {
    NX_CHECK_DRIVER(driver, );
    keyboardDriver = driver;
}

bool Nx_KeyPressed(NxKey key) {
    NX_DRIVER_DISPATCH(keyboardDriver, keyPressed, false, key);
}
bool Nx_KeyActive(NxKey key) {
    NX_DRIVER_DISPATCH(keyboardDriver, keyActive, false, key);
}
bool Nx_KeyReleased(NxKey key) {
    NX_DRIVER_DISPATCH(keyboardDriver, keyReleased, false, key);
}