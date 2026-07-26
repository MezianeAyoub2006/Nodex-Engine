#include "nodex/backend/abstract/texture.h"
#include "nodex/macros/misc.h"

static const NxTextureDriver* textureDriver = NULL;

void Nx_TextureInit(const NxTextureDriver* driver) {
    NX_CHECK_DRIVER(driver, );
    textureDriver = driver;
}

void Nx_TextureLoad(NxTexture* out, const char* path) {
    NX_DRIVER_DISPATCH_VOID(textureDriver, load, out, path);
}

void Nx_TextureLoadRaw(NxTexture* out, const unsigned char* data, size_t size) {
    NX_DRIVER_DISPATCH_VOID(textureDriver, loadRaw, out, data, size);
}

void Nx_TextureUnload(NxTexture* texture) {
    NX_DRIVER_DISPATCH_VOID(textureDriver, unload, texture);
}

void Nx_TextureSetFilter(NxTexture* texture, NxTextureFilter filter) {
    NX_DRIVER_DISPATCH_VOID(textureDriver, setFilter, texture, filter);
}

void Nx_TextureSetWrap(NxTexture* texture, NxTextureWrap wrap) {
    NX_DRIVER_DISPATCH_VOID(textureDriver, setWrap, texture, wrap);
}