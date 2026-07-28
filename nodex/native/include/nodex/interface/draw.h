#ifndef INTERFACE_DRAW_H
#define INTERFACE_DRAW_H

#include "nodex/data/data.h"
#include "nodex/status/status.h"  
#include "nodex/backend/abstract/texture.h"

typedef struct {
    NxTexture* texture;   
    NxRect source;        
    NxRect dest;          
    NxVector2 origin;     
    float rotation;       
    float z_index;
    NxColor tint;         
    int arrival_id;       
} PyDrawTaskFull; 

typedef struct {
    NxTexture* texture;        
    NxRect dest;               
    float z_index;
    NxColor tint;         
    int arrival_id;       
} PyDrawTaskFast; 

typedef struct {
    struct { 
        PyDrawTaskFull tasks[20000]; 
        int ptr; 
    } full;  
    struct {    
        PyDrawTaskFast tasks[20000]; 
        int ptr; 
    } fast; 
} PyDraw; 

#endif 