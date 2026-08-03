#pragma once 

#include "nodex/types/types.h"
#include "nodex/drivers/texture.h"
#include "nodex/drivers/type.h"

typedef struct {
    NxDriverType type; 
    void (*begin_frame)(void);
    void (*end_frame)(void);  
    void (*clear)(NxColor); 

    void (*draw_simple)(
        NxTexture* texture, 
        NxVec2 position
    );

    void (*draw)(
        NxTexture* texture,
        NxVec2 position,  
        float rotation, 
        float scale
    ); 

    void (*draw_full)(
        NxTexture* texture,
        NxRect source, 
        NxRect dest, 
        NxVec2 origin, 
        float rotation, 
        NxColor tint 
    ); 
} NxRendererDriver; 

void Nx_Renderer_Init(const NxRendererDriver* driver);
void Nx_Renderer_BeginFrame(void); 
void Nx_Renderer_EndFrame(void); 
void Nx_Renderer_Clear(NxColor color); 

void Nx_Renderer_DrawSimple(
    NxTexture* texture, 
    NxVec2 position
);

void Nx_Renderer_Draw(
    NxTexture* texture,
    NxVec2 position,  
    float rotation, 
    float scale
); 

void Nx_Renderer_DrawFull(
    NxTexture* texture,
    NxRect source, 
    NxRect dest, 
    NxVec2 origin, 
    float rotation, 
    NxColor tint 
); 