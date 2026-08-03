#include "nodex/drivers/renderer.h"
#include "nodex/status/status.h"
#include "macros.h" 
#include "nodex/macros.h"

#ifdef NX_PERF
    #define TEX_CHECK(texture) NX_NONE()
#else
    #define TEX_CHECK(texture) NX_REQUIRE_NONNULL(texture, NxTexture*)
#endif

static const NxRendererDriver* static_driver = NULL;

void Nx_Renderer_Init(const NxRendererDriver* driver) { 
    NX_DRIVER_CHECK(driver, static_driver, NX_DRIVER_RENDERER, NxRendererDriver*, "Renderer"); 
    static_driver = driver; 
}   

void Nx_Renderer_BeginFrame(void) {
    FULL_DISPATCH_VOID(static_driver, "Renderer", begin_frame); 
}

void Nx_Renderer_EndFrame(void) {
    FULL_DISPATCH_VOID(static_driver, "Renderer", end_frame); 
}

void Nx_Renderer_Clear(NxColor color) { 
    FULL_DISPATCH_VOID(static_driver, "Renderer", clear, 
        color);     
}

void Nx_Renderer_DrawSimple(
    NxTexture* texture, 
    NxVec2 position
) {
    TEX_CHECK(texture);
    FULL_DISPATCH_VOID(static_driver, "Renderer", draw_simple, 
        texture, 
        position); 
}

void Nx_Renderer_Draw(
    NxTexture* texture,
    NxVec2 position,  
    float rotation, 
    float scale
) {
    TEX_CHECK(texture);
    FULL_DISPATCH_VOID(static_driver, "Renderer", draw, 
        texture, 
        position, 
        rotation,
        scale); 
}

void Nx_Renderer_DrawFull(
    NxTexture* texture,
    NxRect source, 
    NxRect dest, 
    NxVec2 origin, 
    float rotation, 
    NxColor tint 
) {
    TEX_CHECK(texture);
    FULL_DISPATCH_VOID(static_driver, "Renderer", draw_full, 
        texture,
        source, 
        dest, 
        origin, 
        rotation, 
        tint); 
}

