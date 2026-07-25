#include "nodex/backend/abstract/texture.h"
#include "nodex/macros/misc.h" 

static const NxTextureDriver* textureDriver = NULL; 

NxStatus Nx_TextureInit(const NxTextureDriver* driver) {
    NX_CHECK_DRIVER(driver);  
    textureDriver = driver;  
    return NX_OKAY;  
}

NxStatus Nx_TextureLoad(NxTexture* out, const char* path) {
    NX_DRIVER_DISPATCH(textureDriver, load, out, path);
}

NxStatus Nx_TextureLoadRaw(NxTexture* out, const unsigned char* data, size_t size) {
    NX_DRIVER_DISPATCH(textureDriver, loadRaw, out, data, size);
}

NxStatus Nx_TextureUnload(NxTexture* texture) {
    NX_DRIVER_DISPATCH(textureDriver, unload, texture);
}

NxStatus Nx_TextureSetFilter(NxTexture* texture, NxTextureFilter filter) {
    NX_DRIVER_DISPATCH(textureDriver, setFilter, texture, filter);
}

NxStatus Nx_TextureSetWrap(NxTexture* texture, NxTextureWrap wrap) {
    NX_DRIVER_DISPATCH(textureDriver, setWrap, texture, wrap);
}
