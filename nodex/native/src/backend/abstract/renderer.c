#include "nodex/backend/abstract/renderer.h"

static const NxRendererDriver* internalRendererDriver;

void Nx_RendererInit(const NxRendererDriver* driver) {
    NX_CHECK_DRIVER(driver, );
    internalRendererDriver = driver;
    if (internalRendererDriver->init)
        internalRendererDriver->init();
}

void Nx_RendererBeginFrame(void) {
    NX_DRIVER_DISPATCH_VOID(internalRendererDriver, beginFrame);
}

void Nx_RendererEndFrame(void) {
    NX_DRIVER_DISPATCH_VOID(internalRendererDriver, endFrame);
}

void Nx_RendererClear(NxColor color) {
    NX_DRIVER_DISPATCH_VOID(internalRendererDriver, clear, color);
}

void Nx_RendererSetBlend(NxBlend blend) {
    NX_DRIVER_DISPATCH_VOID(internalRendererDriver, setBlend, blend);
}

void Nx_RendererDraw(
    const NxTexture* texture,
    NxRect source,
    NxRect dest,
    NxVector2 origin,
    float rotation,
    NxColor tint
) {
    NX_DRIVER_DISPATCH_VOID(
        internalRendererDriver,
        draw,
        texture,
        source, dest,
        origin, rotation,
        tint
    );
}

void Nx_RendererDrawFast(
    const NxTexture* texture,
    NxRect dest,
    NxColor tint
) {
    NX_DRIVER_DISPATCH_VOID(
        internalRendererDriver,
        drawFast,
        texture,
        dest,
        tint
    );
} 

