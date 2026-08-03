#pragma once

#include "nodex/types/types.h" 
#include "nodex/drivers/type.h" 

typedef struct {
    void* raw; 
    NxVec2 size; 
} NxTexture; 

typedef struct {      
    NxDriverType type;   
    NxTexture* (*load)(const char*); 
    void (*unload)(NxTexture*);  
} NxTextureDriver;  

void Nx_Texture_Init(NxTextureDriver* driver); 
NxTexture* Nx_Texture_Load(const char* path);  
void Nx_Texture_Unload(NxTexture* texture); 
 


