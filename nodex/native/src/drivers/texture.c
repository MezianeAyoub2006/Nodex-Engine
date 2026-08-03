#include <stdlib.h>
#include <stdio.h>
#include "nodex/drivers/texture.h"
#include "nodex/status/status.h"
#include "macros.h" 
#include "nodex/macros.h"

static NxTextureDriver* static_driver = NULL; 

void Nx_Texture_Init(NxTextureDriver* driver) {
    NX_DRIVER_CHECK(driver, static_driver, NX_DRIVER_TEXTURE, NxTextureDriver*, "Texture"); 
    static_driver = driver;  
}

NxTexture* Nx_Texture_Load(const char* path) {
    NX_REQUIRE_NONNULL(path, char*);  
    FULL_DISPATCH(static_driver, "Texture", load, NULL, 
        path);  
}

void Nx_Texture_Unload(NxTexture* texture) {
    NX_REQUIRE_NONNULL(texture, NxTexture*);   
    NX_ERROR_IF(!texture->raw, NX_ERR_NULLPTR, 
        "(texture.raw): Excepted non null texture raw data.", 
        return);
    FULL_DISPATCH_VOID(static_driver, "Texture", unload, 
        texture);
}