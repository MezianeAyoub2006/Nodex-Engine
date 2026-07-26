#ifndef KEYBOARD_H
#define KEYBOARD_H

#include <stdbool.h>
#include "nodex/backend/abstract/key.h"
#include "nodex/status/status.h"

typedef struct {
    bool (*keyPressed)(NxKey key);
    bool (*keyReleased)(NxKey key);
    bool (*keyActive)(NxKey key);
} NxKeyboardDriver;

void Nx_KeyboardInit(const NxKeyboardDriver* driver);

bool Nx_KeyPressed(NxKey key);
bool Nx_KeyActive(NxKey key);
bool Nx_KeyReleased(NxKey key);

#endif