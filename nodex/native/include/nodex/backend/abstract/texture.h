#ifndef TEXTURE_H
#define TEXTURE_H

#include <stddef.h>
#include "nodex/status/status.h"

typedef enum {
    NX_FORMAT_UNKNOWN = 0,
    NX_FORMAT_R8,
    NX_FORMAT_R8G8B8,
    NX_FORMAT_R8G8B8A8,
    NX_FORMAT_R16F,
    NX_FORMAT_R32F
} NxTextureFormat;

typedef enum {
    NX_WRAP_REPEAT = 0,
    NX_WRAP_CLAMP,
    NX_WRAP_MIRROR_REPEAT,
    NX_WRAP_MIRROR_CLAMP
} NxTextureWrap;

typedef enum {
    NX_FILTER_POINT = 0,
    NX_FILTER_BILINEAR,
    NX_FILTER_TRILINEAR,
    NX_FILTER_ANISOTROPIC_4X
} NxTextureFilter;

typedef struct {
    NxTextureFilter filter;
    NxTextureWrap wrap;
    NxTextureFormat pixelFormat;
} NxTextureProp;

typedef struct {
    void* raw;
    int width, height;
    NxTextureProp prop;
} NxTexture;

typedef struct {
    void (*load)(NxTexture*, const char*);
    void (*loadRaw)(NxTexture*, const unsigned char*, size_t);
    void (*unload)(NxTexture*);
    void (*setFilter)(NxTexture*, NxTextureFilter);
    void (*setWrap)(NxTexture*, NxTextureWrap);
    void (*setFormat)(NxTexture*, NxTextureFormat);
} NxTextureDriver;

void Nx_TextureInit(const NxTextureDriver* driver);
void Nx_TextureLoad(NxTexture* out, const char* path);
void Nx_TextureLoadRaw(NxTexture* out, const unsigned char* data, size_t size);
void Nx_TextureUnload(NxTexture* texture);
void Nx_TextureSetFilter(NxTexture* texture, NxTextureFilter filter);
void Nx_TextureSetWrap(NxTexture* texture, NxTextureWrap wrap);

#endif