#include <stdlib.h>
#include "raylib/raylib.h"
#include "nodex/backend/raylib/raylib_texture.h"
#include "nodex/status/status.h"

static NxTextureFormat RaylibFormatToNodex(int raylibFormat) {
    switch (raylibFormat) {
        case PIXELFORMAT_UNCOMPRESSED_GRAYSCALE:
            return NX_FORMAT_R8;
        case PIXELFORMAT_UNCOMPRESSED_R8G8B8:
            return NX_FORMAT_R8G8B8;
        case PIXELFORMAT_UNCOMPRESSED_R8G8B8A8:
            return NX_FORMAT_R8G8B8A8;
        default:
            return NX_FORMAT_R8G8B8A8;
    }
}

static void Raylib_TextureLoad(NxTexture* out, const char* path) {
    if (!out || !path) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Texture out pointer or path is NULL");
        return;
    }
    Texture2D* tex = malloc(sizeof(Texture2D));
    if (!tex) {
        Nx_SetStatus(NX_ERR_OUT_OF_MEMORY, "Failed to allocate Texture2D");
        return;
    }
    *tex = LoadTexture(path);
    if (tex->id == 0) {
        free(tex);
        Nx_SetStatus(NX_ERR_INVALID_ARGS, "Failed to load texture from path");
        return;
    }
    out->prop = (NxTextureProp){
        .filter = NX_FILTER_POINT,
        .wrap = NX_WRAP_CLAMP,
        .pixelFormat = RaylibFormatToNodex(tex->format)
    };
    out->width = tex->width;
    out->height = tex->height;
    out->raw = tex;
}

static void Raylib_TextureUnload(NxTexture* out) {
    if (!out) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Texture out pointer is NULL");
        return;
    }
    if (!out->raw) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Texture raw data is NULL");
        return;
    }
    UnloadTexture(*(Texture2D*)(out->raw));
    free(out->raw);
    out->raw = NULL;
}

static const NxTextureDriver raylibDriver = {
    .load = &Raylib_TextureLoad,
    .unload = &Raylib_TextureUnload,
    .loadRaw = NULL,
    .setFilter = NULL,
    .setWrap = NULL
};

const NxTextureDriver* Nx_GetRaylibTextureDriver(void) {
    return &raylibDriver;
}