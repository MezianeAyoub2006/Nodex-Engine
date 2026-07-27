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
    void (*init)(void);
    void (*beginFrame)(void);
    void (*endFrame)(void);
    void (*clear)(NxColor);
    void (*draw)(const NxTexture*, NxRect, NxRect, NxVector2, float, NxColor);
    void (*drawFast)(const NxTexture*, NxRect, NxColor); 
    void (*setBlend)(NxBlend);
} NxRendererDriver;

void Nx_RendererInit(const NxRendererDriver* driver);
void Nx_RendererBeginFrame(void);
void Nx_RendererEndFrame(void);
void Nx_RendererClear(NxColor color);

void Nx_RendererDraw(
    const NxTexture* texture,
    NxRect source, NxRect dest,       
    NxVector2 origin, float rotation, 
    NxColor tint
);

void Nx_RendererDrawFast(
    const NxTexture* texture,
    NxRect dest,        
    NxColor tint
);

void Nx_RendererSetBlend(NxBlend blend);

#endif