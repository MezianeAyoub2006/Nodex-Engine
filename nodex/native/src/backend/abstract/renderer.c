#include "nodex/backend/abstract/renderer.h"

static const NxRendererDriver* internalRendererDriver; 

NxStatus Nx_RendererInit(const NxRendererDriver* driver) {
    NX_CHECK_DRIVER(driver); 
    internalRendererDriver = driver; 
    if (internalRendererDriver->init) 
        return internalRendererDriver->init();
    return NX_OKAY;
}

NxStatus Nx_RendererBeginFrame(void) { 
    NX_DRIVER_DISPATCH(internalRendererDriver, beginFrame); 
}

NxStatus Nx_RendererEndFrame(void) { 
    NX_DRIVER_DISPATCH(internalRendererDriver, endFrame); 
}

NxStatus Nx_RendererClear(NxColor color) { 
    NX_DRIVER_DISPATCH(internalRendererDriver, clear, color); 
}                 

NxStatus Nx_RendererSetBlend(NxBlend blend) {
    NX_DRIVER_DISPATCH(internalRendererDriver, setBlend, blend);
}

NxStatus Nx_RendererDraw(
    const NxTexture* texture, 
    NxRect source, 
    NxRect dest, 
    NxVector2 origin, 
    float rotation, 
    NxColor tint
) {
    NX_DRIVER_DISPATCH(
        internalRendererDriver, 
        draw, 
        texture, 
        source, dest, 
        origin, rotation, 
        tint
    );
}