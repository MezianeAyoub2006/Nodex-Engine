#include "nodex/drivers/ray/ray_keyboard.h"

#include "raylib/raylib.h" 

static const int translation_table[NX_KEY_NUMBER] = {
    [NX_KEY_NULL] = 0,
    [NX_KEY_ZERO] = KEY_ZERO,
    [NX_KEY_ONE] = KEY_ONE,
    [NX_KEY_TWO] = KEY_TWO,
    [NX_KEY_THREE] = KEY_THREE,
    [NX_KEY_FOUR] = KEY_FOUR,
    [NX_KEY_FIVE] = KEY_FIVE,
    [NX_KEY_SIX] = KEY_SIX,
    [NX_KEY_SEVEN] = KEY_SEVEN,
    [NX_KEY_EIGHT]= KEY_EIGHT,
    [NX_KEY_NINE] = KEY_NINE,
    [NX_KEY_A] = KEY_A,
    [NX_KEY_B] = KEY_B,
    [NX_KEY_C] = KEY_C,
    [NX_KEY_D] = KEY_D,
    [NX_KEY_E] = KEY_E,
    [NX_KEY_F] = KEY_F,
    [NX_KEY_G] = KEY_G,
    [NX_KEY_H] = KEY_H,
    [NX_KEY_I] = KEY_I,
    [NX_KEY_J] = KEY_J,
    [NX_KEY_K] = KEY_K,
    [NX_KEY_L] = KEY_L,
    [NX_KEY_M] = KEY_M,
    [NX_KEY_N] = KEY_N,
    [NX_KEY_O] = KEY_O,
    [NX_KEY_P] = KEY_P,
    [NX_KEY_Q] = KEY_Q,
    [NX_KEY_R] = KEY_R,
    [NX_KEY_S] = KEY_S,
    [NX_KEY_T] = KEY_T,
    [NX_KEY_U] = KEY_U,
    [NX_KEY_V] = KEY_V,
    [NX_KEY_W] = KEY_W,
    [NX_KEY_X] = KEY_X,
    [NX_KEY_Y] = KEY_Y,
    [NX_KEY_Z] = KEY_Z,
    [NX_KEY_UP] = KEY_UP,
    [NX_KEY_DOWN] = KEY_DOWN,
    [NX_KEY_LEFT] = KEY_LEFT,
    [NX_KEY_RIGHT] = KEY_RIGHT,
    [NX_KEY_SPACE] = KEY_SPACE,
    [NX_KEY_ENTER] = KEY_ENTER,
    [NX_KEY_ESCAPE] = KEY_ESCAPE,
    [NX_KEY_TAB] = KEY_TAB,
    [NX_KEY_BACKSPACE] = KEY_BACKSPACE,
    [NX_KEY_INSERT] = KEY_INSERT,
    [NX_KEY_DELETE] = KEY_DELETE,
    [NX_KEY_HOME] = KEY_HOME,
    [NX_KEY_END] = KEY_END,
    [NX_KEY_PAGE_UP] = KEY_PAGE_UP,
    [NX_KEY_PAGE_DOWN] = KEY_PAGE_DOWN,
    [NX_KEY_F1] = KEY_F1,
    [NX_KEY_F2] = KEY_F2,
    [NX_KEY_F3] = KEY_F3,
    [NX_KEY_F4] = KEY_F4,
    [NX_KEY_F5] = KEY_F5,
    [NX_KEY_F6] = KEY_F6,
    [NX_KEY_F7] = KEY_F7,
    [NX_KEY_F8] = KEY_F8,
    [NX_KEY_F9] = KEY_F9,
    [NX_KEY_F10] = KEY_F10,
    [NX_KEY_F11] = KEY_F11,
    [NX_KEY_F12] = KEY_F12,
    [NX_KEY_LEFT_SHIFT] = KEY_LEFT_SHIFT,
    [NX_KEY_RIGHT_SHIFT] = KEY_RIGHT_SHIFT,
    [NX_KEY_LEFT_CONTROL] = KEY_LEFT_CONTROL,
    [NX_KEY_RIGHT_CONTROL] = KEY_RIGHT_CONTROL,
    [NX_KEY_LEFT_ALT] = KEY_LEFT_ALT,
    [NX_KEY_RIGHT_ALT] = KEY_RIGHT_ALT,
    [NX_KEY_LEFT_SUPER] = KEY_LEFT_SUPER,
    [NX_KEY_RIGHT_SUPER] = KEY_RIGHT_SUPER,
    [NX_KEY_CAPS_LOCK] = KEY_CAPS_LOCK,
    [NX_KEY_SCROLL_LOCK] = KEY_SCROLL_LOCK,
    [NX_KEY_NUM_LOCK] = KEY_NUM_LOCK,
    [NX_KEY_APOSTROPHE] = KEY_APOSTROPHE,
    [NX_KEY_COMMA] = KEY_COMMA,
    [NX_KEY_MINUS] = KEY_MINUS,
    [NX_KEY_PERIOD] = KEY_PERIOD,
    [NX_KEY_SLASH] = KEY_SLASH,
    [NX_KEY_SEMICOLON] = KEY_SEMICOLON,
    [NX_KEY_EQUAL] = KEY_EQUAL,
    [NX_KEY_LEFT_BRACKET] = KEY_LEFT_BRACKET,
    [NX_KEY_BACKSLASH] = KEY_BACKSLASH,
    [NX_KEY_RIGHT_BRACKET] = KEY_RIGHT_BRACKET,
    [NX_KEY_GRAVE] = KEY_GRAVE
};


int Nx_To_RayKey(NxKey key) {
    if (key < 0 || key >= NX_KEY_NUMBER) {
        return 0; 
    }
    return translation_table[key];
}

bool Raylib_GetPressed(NxKey key) {
    return IsKeyPressed(Nx_To_RayKey(key)); 
}

bool Raylib_GetActive(NxKey key) {
    return IsKeyDown(Nx_To_RayKey(key)); 
}

bool Raylib_GetReleased(NxKey key) {
    return IsKeyReleased(Nx_To_RayKey(key)); 
}

static NxKeyboardDriver static_driver = {
    .type = NX_DRIVER_KEYBOARD, 
    .get_active = &Raylib_GetActive,
    .get_pressed = &Raylib_GetPressed,
    .get_released = &Raylib_GetReleased 
};

const NxKeyboardDriver* Raylib_KeyboardDriver(void) {
    return &static_driver;
}

