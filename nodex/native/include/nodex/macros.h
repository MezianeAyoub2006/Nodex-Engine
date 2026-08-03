#pragma once

#include "nodex/status/macros.h"

#define NX_TEXTURE_UNLOAD_SAFE(tex_ptr) \
    do { \
        if (tex_ptr && *tex_ptr) { \
            Nx_Texture_Unload(*tex_ptr); \
            *tex_ptr = NULL; \
        } \
    } while(0)

#define NX_REQUIRE_NONNULL(ptr, type, ...)                                              \
    NX_ERROR_IF(!(ptr), NX_ERR_ARGS,                                                    \
        "Expected a valid " #type ", got NULL.",                                        \
        return __VA_ARGS__)

#define NX_REQUIRE_POSITIVE_VEC2(vec, placeholder, ...) \
    NX_ERROR_IF((vec).x <= 0 || (vec).y <= 0, NX_ERR_ARGS,                              \
        placeholder "Size dimensions must be strictly positive (got <= 0).",            \
        return __VA_ARGS__)    
