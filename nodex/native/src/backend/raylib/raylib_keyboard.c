#include <stdlib.h>
#include "raylib/raylib.h"
#include "nodex/backend/raylib/raylib_keyboard.h"

#include "raylib/raylib.h"
#include "nodex/backend/raylib/raylib_keyboard.h"

static const KeyboardKey nxKeyToRaylibTable[NX_KEY_NUMBER] = {
    [NX_K_UNKNOWN] = KEY_NULL,
    [NX_K_LEFT] = KEY_LEFT,
    [NX_K_RIGHT] = KEY_RIGHT,
    [NX_K_UP] = KEY_UP,
    [NX_K_DOWN] = KEY_DOWN,
    [NX_K_A] = KEY_A,
    [NX_K_B] = KEY_B,
    [NX_K_C] = KEY_C,
    [NX_K_D] = KEY_D,
    [NX_K_E] = KEY_E,
    [NX_K_F] = KEY_F,
    [NX_K_G] = KEY_G,
    [NX_K_H] = KEY_H, 
    [NX_K_I] = KEY_I,
    [NX_K_J] = KEY_J,
    [NX_K_K] = KEY_K,
    [NX_K_L] = KEY_L,
    [NX_K_M] = KEY_M,
    [NX_K_N] = KEY_N,
    [NX_K_O] = KEY_O,
    [NX_K_P] = KEY_P,
    [NX_K_Q] = KEY_Q,
    [NX_K_R] = KEY_R,
    [NX_K_S] = KEY_S,
    [NX_K_T] = KEY_T,
    [NX_K_U] = KEY_U,
    [NX_K_V] = KEY_V,
    [NX_K_W] = KEY_W,
    [NX_K_X] = KEY_X,
    [NX_K_Y] = KEY_Y,
    [NX_K_Z] = KEY_Z,
    [NX_K_0] = KEY_ZERO,
    [NX_K_1] = KEY_ONE,
    [NX_K_2] = KEY_TWO,
    [NX_K_3] = KEY_THREE,
    [NX_K_4] = KEY_FOUR,
    [NX_K_5] = KEY_FIVE,
    [NX_K_6] = KEY_SIX,
    [NX_K_7] = KEY_SEVEN,
    [NX_K_8] = KEY_EIGHT,
    [NX_K_9] = KEY_NINE,
    [NX_K_SPACE] = KEY_SPACE,
    [NX_K_ENTER] = KEY_ENTER,
    [NX_K_ESCAPE] = KEY_ESCAPE,
    [NX_K_TAB] = KEY_TAB,
    [NX_K_BACKSPACE] = KEY_BACKSPACE,
    [NX_K_LEFT_SHIFT] = KEY_LEFT_SHIFT,
    [NX_K_RIGHT_SHIFT] = KEY_RIGHT_SHIFT,
    [NX_K_LEFT_CONTROL] = KEY_LEFT_CONTROL,
    [NX_K_RIGHT_CONTROL] = KEY_RIGHT_CONTROL,
    [NX_K_LEFT_ALT] = KEY_LEFT_ALT,
    [NX_K_RIGHT_ALT] = KEY_RIGHT_ALT,
};


static KeyboardKey NodexToRaylibKey(NxKey key) {
    if (key < 0 || key >= NX_KEY_NUMBER) {
        return KEY_NULL;
    }
    return nxKeyToRaylibTable[key];
}

static bool Raylib_KeyPressed(NxKey key) {
    return IsKeyPressed(NodexToRaylibKey(key)); 
}

static bool Raylib_KeyActive(NxKey key) {
    return IsKeyDown(NodexToRaylibKey(key)); 
}

static bool Raylib_KeyReleased(NxKey key) {
    return IsKeyReleased(NodexToRaylibKey(key)); 
}

static NxKeyboardDriver keyboardDriver = {
    .keyPressed = &Raylib_KeyPressed,
    .keyActive = &Raylib_KeyActive,
    .keyReleased = &Raylib_KeyReleased
};

const NxKeyboardDriver* Nx_GetRaylibKeyboardDriver(void) {
    return &keyboardDriver; 
}
