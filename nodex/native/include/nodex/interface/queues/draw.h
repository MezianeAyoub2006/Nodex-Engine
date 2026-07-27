#ifndef DRAW_QUEUE_H
#define DRAW_QUEUE_H

#include "nodex/backend/abstract/texture.h"
#include "nodex/data/data.h"

typedef struct {
    NxTexture* texture;   
    NxRect source;        
    NxRect dest;          
    NxVector2 origin;     
    float rotation;       
    float z_index;
    NxColor tint;         
    int arrival_id;       
} NxDrawTask;

typedef struct { 
    NxDrawTask drawTasks[20000]; 
    int ptr; 
} NxDrawQueue;

typedef struct {
    NxTexture* texture;
    NxRect dest; 
    float z_index; 
    int arrival_id; 
    NxColor tint; 
} NxDrawTaskFast; 

typedef struct {    
    NxDrawTaskFast drawTasks[20000]; 
    int ptr; 
} NxDrawQueueFast; 

#endif 

