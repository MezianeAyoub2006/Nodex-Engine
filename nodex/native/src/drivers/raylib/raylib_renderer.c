#include <math.h>
#include "raylib/raylib.h"
#include "nodex/drivers/ray/ray_renderer.h"
#include "nodex/drivers/window.h"
#include "../macros.h"

static RenderTexture2D target;

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

void Raylib_Renderer_SetVirtualSize(NxVec2 virtual_size) {
    if (target.id != 0) 
        UnloadRenderTexture(target);
    target = LoadRenderTexture((int)virtual_size.x, (int)virtual_size.y);
    SetTextureFilter(target.texture, TEXTURE_FILTER_POINT);
}

static void Raylib_Renderer_BeginFrame(void) {
    BeginTextureMode(target);
}

static void Raylib_Renderer_EndFrame(void) {
    EndTextureMode();
    NxWindow* window =  Nx_Window_Get(); 
    int screen_w = GetScreenWidth();
    int screen_h = GetScreenHeight();

    float virtual_w = (float)target.texture.width;
    float virtual_h = (float)target.texture.height;

    float scale = fminf(
        (float)screen_w / virtual_w,
        (float)screen_h / virtual_h
    );

    float scale_ratio = (window->stretch) ? (window->scale.x / window->scale.y) : 1; 
    float dst_w, dst_h; 
    if ((window->fullscreen) || (scale_ratio > 1)){
        dst_w = virtual_w * scale * scale_ratio;
        dst_h = virtual_h * scale; 
    } else {
        dst_w = virtual_w * scale;
        dst_h = virtual_h * scale / scale_ratio; 
    }
  

    Rectangle src = (Rectangle){
        0.0f, 0.0f,
        virtual_w,
        -virtual_h 
    };

    Rectangle dst = (Rectangle){
        (screen_w - dst_w) * 0.5f,
        (screen_h - dst_h) * 0.5f,
        dst_w,
        dst_h
    };

    BeginDrawing();
    ClearBackground(BLACK); 
    DrawTexturePro(target.texture, src, dst, (Vector2){0, 0}, 0.0f, WHITE);
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