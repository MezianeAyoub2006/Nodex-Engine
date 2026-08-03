#include "raylib/raylib.h"
#include "nodex/drivers/ray/ray_renderer.h"
#include "../macros.h"

static Vector2 Ray_Vector2(NxVec2 vec2) {
    return (Vector2){
        .x = vec2.x, 
        .y = vec2.y 
    };  
}

static Rectangle Ray_Rectangle(NxRect rectangle) {
    return (Rectangle) {
        .x = rectangle.x, 
        .y = rectangle.y, 
        .width = rectangle.w, 
        .height = rectangle.h
    }; 
}

static Color Ray_Color(NxColor color) {
    return (Color){
        .r = color.r, 
        .g = color.g,
        .b = color.b,
        .a = color.a  
    }; 
}

static void Raylib_Renderer_BeginFrame(void) {
    BeginDrawing();  
}

static void Raylib_Renderer_EndFrame(void) {
    EndDrawing();   
}

static void Raylib_Renderer_Clear(NxColor color) {
    ClearBackground(Ray_Color(color)); 
}

static void Raylib_Renderer_DrawSimple(
    NxTexture* texture, 
    NxVec2 position
) {
    DrawTexture(
        *(Texture2D*)texture->raw, 
        (int)position.x, (int)position.y, 
        WHITE 
    ); 
}

static void Raylib_Renderer_Draw(
    NxTexture* texture,
    NxVec2 position,
    float rotation, 
    float scale
) {
    DrawTextureEx(
        *(Texture2D*)texture->raw, 
        Ray_Vector2(position), 
        rotation, scale, 
        WHITE 
    ); 
}

static void Raylib_Renderer_DrawFull(
    NxTexture* texture,
    NxRect source, 
    NxRect dest, 
    NxVec2 origin, 
    float rotation, 
    NxColor tint 
) {
    DrawTexturePro(
        *(Texture2D*)texture->raw, 
        Ray_Rectangle(source),
        Ray_Rectangle(dest),
        Ray_Vector2(origin), 
        rotation,
        Ray_Color(tint)
    ); 
}

static NxRendererDriver static_driver = {
    .type = NX_DRIVER_RENDERER, 
    .begin_frame = &Raylib_Renderer_BeginFrame,
    .clear = &Raylib_Renderer_Clear,
    .draw = &Raylib_Renderer_Draw,
    .draw_full = &Raylib_Renderer_DrawFull, 
    .draw_simple = &Raylib_Renderer_DrawSimple,
    .end_frame = &Raylib_Renderer_EndFrame, 
}; 

const NxRendererDriver* Raylib_RendererDriver(void) {
    return &static_driver; 
}
