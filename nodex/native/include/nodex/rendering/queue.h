#pragma once 

#include "nodex/rendering/tasks.h"

typedef enum {
    TASK_NORMAL, 
    TASK_SIMPLE,
    TASK_FULL 
} NxTaskType; 

typedef struct {
    NxTaskType type;     
    union {
        NxTaskNormal normal; 
        NxTaskSimple simple;
        NxTaskFull full; 
    }; 
    int order; 
} NxRenderingTask;

typedef struct {
    NxRenderingTask tasks[10000];
    uint32_t count; 
} NxRenderingQueue;

NxRenderingQueue* Nx_RenderingQueue_Get(void);
void Nx_RenderingQueue_Update(void); 