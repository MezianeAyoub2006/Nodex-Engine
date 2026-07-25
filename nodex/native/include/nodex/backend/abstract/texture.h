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
    NxStatus (*load)(NxTexture*, const char* path); 
    NxStatus (*loadRaw)(NxTexture*, const unsigned char* data, size_t size);
    NxStatus (*unload)(NxTexture*);
    NxStatus (*setFilter)(NxTexture*, NxTextureFilter filter);  
    NxStatus (*setWrap)(NxTexture*, NxTextureWrap wrap);
    NxStatus (*setFormat)(NxTexture*, NxTextureFormat format); 
} NxTextureDriver;

NxStatus Nx_TextureInit(const NxTextureDriver* driver); 
NxStatus Nx_TextureLoad(NxTexture* out, const char* path);
NxStatus Nx_TextureLoadRaw(NxTexture* out, const unsigned char* data, size_t size); 
NxStatus Nx_TextureUnload(NxTexture* texture);
NxStatus Nx_TextureSetFilter(NxTexture* texture, NxTextureFilter filter); 
NxStatus Nx_TextureSetWrap(NxTexture* texture, NxTextureWrap wrap); 

#endif 