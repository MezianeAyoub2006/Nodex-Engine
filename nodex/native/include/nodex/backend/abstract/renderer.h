#ifndef RENDERER_H
#define RENDERER_H

#include "nodex/macros/misc.h"
#include "nodex/backend/abstract/texture.h"
#include "nodex/data/rect.h"
#include "nodex/data/vec2.h"
#include "nodex/data/color.h"

typedef enum {
    NX_BLEND_ALPHA = 0,
    NX_BLEND_ADDITIVE,
    NX_BLEND_MULTIPLIED,
    NX_BLEND_ADD_COLORS
} NxBlend;

typedef struct {
    NxStatus (*init)(void);  
    NxStatus (*beginFrame)(void);
    NxStatus (*endFrame)(void);
    NxStatus (*clear)(NxColor color);
    NxStatus (*draw)(
        const NxTexture* texture, 
        NxRect source, 
        NxRect dest, 
        NxVector2 origin, 
        float rotation, 
        NxColor tint
    );
    NxStatus (*setBlend)(NxBlend blend);
} NxRendererDriver;

NxStatus Nx_RendererInit(const NxRendererDriver* driver); 
NxStatus Nx_RendererBeginFrame(void); 
NxStatus Nx_RendererEndFrame(void); 
NxStatus Nx_RendererClear(NxColor color);
NxStatus Nx_RendererDraw(
    const NxTexture* texture, 
    NxRect source, 
    NxRect dest, 
    NxVector2 origin, 
    float rotation, 
    NxColor tint
); 
NxStatus Nx_RendererSetBlend(NxBlend blend); 

#endif