#include "raylib/raylib.h"
#include "nodex/backend/abstract/texture.h"
#include "nodex/backend/raylib/raylib_renderer.h"
#include "nodex/status/status.h"

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

static void Raylib_RendererBeginFrame(void) {
    BeginDrawing();
}

static void Raylib_RendererEndFrame(void) {
    EndDrawing();
}

static void Raylib_RendererDraw(
    const NxTexture* texture,
    NxRect source,
    NxRect dest,
    NxVector2 origin,
    float rotation,
    NxColor tint
) {
    if (!texture) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Texture is NULL");
        return;
    }
    if (!texture->raw) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Texture raw data is NULL");
        return;
    }
    DrawTexturePro(
        *(Texture2D*)texture->raw,
        NodexToRayRect(source),
        NodexToRayRect(dest),
        NodexToRayVec2(origin),
        rotation,
        NodexToRayColor(tint)
    );
}

static void Raylib_RendererClear(NxColor color) {
    ClearBackground(NodexToRayColor(color));
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