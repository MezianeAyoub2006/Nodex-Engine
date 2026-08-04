#pragma once 

#include <stdbool.h>
#include "nodex/types/types.h"
#include "nodex/drivers/type.h"

#define NX_FLAG_VSYNC (1 << 0)

typedef struct {
    NxVec2 virtual_size;    
    NxVec2 scale;
    int flags; 
    int target_fps; 
    const char* caption; 
    bool stretch;
    bool fullscreen; 
} NxWindow; 

typedef struct {
    NxDriverType type; 
    void (*init)(NxWindow*);   
    void (*set_virtual_size)(NxWindow*); 
    void (*set_scale)(NxWindow*); 
    void (*set_target_fps)(NxWindow*); 
    void (*set_caption)(NxWindow*); 
    void (*toggle_fullscreen)(NxWindow*); 
    bool (*should_close)(NxWindow*); 
} NxWindowDriver; 

const NxWindow* Nx_Window_Get(void);
void Nx_Window_Init(const NxWindowDriver* driver, NxWindow window); 
void Nx_Window_SetVirtualSize(NxVec2 virtual_size); 
void Nx_Window_SetScale(NxVec2 scale);
void Nx_Window_SetTargetFps(int target_fps);  
void Nx_Window_SetCaption(const char* caption); 
void Nx_ToggleFullscreen(void); 
bool Nx_Window_ShouldClose(void); 








