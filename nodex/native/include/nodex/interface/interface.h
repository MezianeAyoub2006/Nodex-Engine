#ifndef INTERFACE_H
#define INTERFACE_H 

#include <stdbool.h>
#include "nodex/backend/abstract/texture.h"
#include "nodex/interface/draw.h"
#include "nodex/interface/input.h"

typedef struct {
    struct {
        PyKeyboardRead keyboard; 

        struct {
            bool shouldClose; 
        } flags;

        struct {
            int fps; 
            float dt; 
        } time;
      
        struct {
            NxStatus last;
            const char* message;
        } status; 
    } read; 
    struct {
        PyDraw draw; 
        PyKeyboardRequested keys; 
        struct {
            bool statusConsumed; 
        } flags;
      
    } write;
} PyInterface; 

PyInterface* Nx_GetInterface(void); 
void Nx_Update(void);

#endif 