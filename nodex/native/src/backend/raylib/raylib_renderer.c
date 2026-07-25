#include "raylib/raylib.h"
#include "nodex/backend/abstract/texture.h" 
#include "nodex/backend/raylib/raylib_renderer.h"

static Rectangle NodexToRayRect(NxRect rect){ 
    return (Rectangle){
        .x = rect.x, 
        .y = rect.y, 
        .width = rect.width, 
        .height = rect.height 
    }; 
}

static Vector2 NodexToRayVec2(NxVector2 vec){ 
    return (Vector2){
        .x = vec.x, 
        .y = vec.y 
    }; 
}

static Color NodexToRayColor(NxColor color) {
    return (Color){
        .r = color.r, 
        .g = color.g,
        .b = color.b,
        .a = color.a
    };
}

static NxStatus Raylib_RendererBeginFrame(void) {
    BeginDrawing(); 
    return NX_OKAY;
}

static NxStatus Raylib_RendererEndFrame(void) {
    EndDrawing(); 
    return NX_OKAY; 
}

static NxStatus Raylib_RendererDraw(    
    const NxTexture* texture, 
    NxRect source, 
    NxRect dest, 
    NxVector2 origin, 
    float rotation, 
    NxColor tint
) {
    if (!texture)
        return NX_ERR_NULLPTR;
    if (!texture->raw)
        return NX_ERR_NULLPTR; 
    DrawTexturePro(
        *(Texture2D*)texture->raw, 
        NodexToRayRect(source),
        NodexToRayRect(dest), 
        NodexToRayVec2(origin), 
        rotation, 
        NodexToRayColor(tint)
    ); 
    return NX_OKAY;
}

static NxStatus Raylib_RendererClear(NxColor color) {
    ClearBackground(NodexToRayColor(color)); 
    return NX_OKAY; 
}

static NxRendererDriver rendererDriver = {
    .beginFrame = &Raylib_RendererBeginFrame,
    .clear = &Raylib_RendererClear,
    .draw = &Raylib_RendererDraw,
    .endFrame = &Raylib_RendererEndFrame,
    .init = NULL,
    .setBlend = NULL 
};

const NxRendererDriver* Nx_GetRaylibRendererDriver(void) {
    return &rendererDriver; 
}
