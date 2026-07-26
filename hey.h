#ifndef NODEX_H
#define NODEX_H

#ifndef STATUS_H
#define STATUS_H

/*  NxState is mainly a return value for functions to indicate
to the engine the state of their execution, if everything went okay,
you will get NX_OKAY, if the developper want to warn you about some
shi, you will get NX_WARN_... . If the function completly failed,
you will get NX_ERR_... . */
typedef enum {
    NX_OKAY = 0,                    // shi fine.

    NX_ERR,
    /* --------------- ERRORS --------------- */
    NX_ERR_NULLPTR,                 // shi obvious. (unexpected NULL pointer passed.).
    NX_ERR_INVALID_DRIVER_INIT,     // Driver struct is invalid or incomplete during init.
    NX_ERR_DRIVER_NULL,
    NX_ERR_INVALID_ARGS,
    NX_ERR_OUT_OF_MEMORY,           // Why even explain ? malloc failed, weak ass ram.

    NX_WARN,
    /* -------------- WARNINGS --------------- */
    NX_WARN_FEATURE_NOT_SUPPORTED,  // When a driver doesn't implement a feature.

    NX_STATUS_NUMBER
} NxStatus;

/*Checks if a status is an error.
[ Examples ]
NX_IS_ERROR(NX_ERR_NULLPTR) -> 1
NX_IS_ERROR(NX_ERR) -> 1
NX_IS_ERROR(NX_OKAY) -> 0*/
#define NX_IS_ERROR(status) \
    (((status) != NX_OKAY) && ((status) < NX_WARN))
    
/*Checks if a status is a warning.
[ Examples ]
NX_IS_WARNING(NX_WARN) -> 1
NX_IS_WARNING(NX_ERR_OUT_OF_MEMORY) ->  0
NX_IS_WARNING(NX_OKAY) -> 0*/
#define NX_IS_WARNING(status) \
     ((status) >= NX_WARN)

    
/* Sets the global status of the engine execution */
void Nx_SetStatus(NxStatus status, const char* message);

/* Retrieves the last status set by Nx_SetStatus. */
NxStatus Nx_GetStatus(void);

/* Retrieves the message tied to the last status set by Nx_SetStatus. */
const char* Nx_GetStatusMessage(void);

#endif
#ifndef MISC_H
#define MISC_H



/* Checks if (w, h) surface has negative size */
#define NX_CHECK_NEGSIZE(w, h, retval)                                      \
    do {                                                                    \
        if ((w) <= 0 || (h) <= 0) {                                         \
            Nx_SetStatus(NX_ERR_INVALID_ARGS, "Negative or null size");     \
            return retval;                                                  \
        }                                                                   \
    } while (0)

/* Checks if a specified driver is valid */
#define NX_CHECK_DRIVER(driver, retval)                                     \
    do {                                                                    \
        if (!(driver)) {                                                    \
            Nx_SetStatus(NX_ERR_DRIVER_NULL, "Driver is NULL");             \
            return retval;                                                  \
        }                                                                   \
    } while (0)

/* Checks if a feature if implemented */
#define NX_CHECK_FEATURE(func_ptr, retval)                                  \
    do {                                                                    \
        if (!(func_ptr)) {                                                  \
            Nx_SetStatus(                                                   \
                NX_WARN_FEATURE_NOT_SUPPORTED,                              \
                "Feature not supported by driver"                           \
            );                                                              \
            return retval;                                                  \
        }                                                                   \
    } while (0)

/* Dispach a function into a driver, forwarding its return value */
#define NX_DRIVER_DISPATCH(driver, fn_name, retval, ...)                    \
    do {                                                                    \
        NX_CHECK_DRIVER(driver, retval);                                    \
        NX_CHECK_FEATURE((driver)->fn_name, retval);                        \
        return (driver)->fn_name(__VA_ARGS__);                              \
    } while (0)

/* Dispatch a function into a driver, without forwarding a value (void callers) */
#define NX_DRIVER_DISPATCH_VOID(driver, fn_name, ...)                       \
    do {                                                                    \
        NX_CHECK_DRIVER(driver, );                                          \
        NX_CHECK_FEATURE((driver)->fn_name, );                              \
        (driver)->fn_name(__VA_ARGS__);                                     \
        return;                                                             \
    } while (0)

#endif
#ifndef WINDOW_H
#define WINDOW_H



typedef struct {
    int virtualWidth; int virtualHeight;
    float scale_X; float scale_Y;
    bool fullscreen; bool vsync;
    const char* title;
} NxWindow;

typedef struct {
    void (*init)(NxWindow*);
    void (*setVirtualSize)(NxWindow*);
    void (*setScale)(NxWindow*);
    void (*setTitle)(NxWindow*);
    void (*toggleFullscreen)(NxWindow*);
} NxWindowDriver;

const NxWindow* Nx_WindowGet(void);
void Nx_WindowInit(const NxWindowDriver* driver, NxWindow window);
void Nx_WindowSetVirtualSize(int virtualWidth, int virtualHeight);
void Nx_WindowSetScale(float scale_X, float scale_Y);
void Nx_WindowSetTitle(const char* title);
void Nx_WindowToggleFullscreen(void);

#endif
#ifndef NX_POOL_H
#define NX_POOL_H



#define NX_DEFINE_POOL(T, NAME)                                                     \
typedef struct {                                                                    \
    T* data;                                                                        \
    uint32_t* generation;                                                           \
    bool* active;                                                                   \
    uint32_t* free_list;                                                            \
    size_t capacity;                                                                \
    size_t free_count;                                                              \
} NAME##Pool;                                                                       \
\
static NxStatus NAME##_Pool_Init(NAME##Pool* pool, size_t capacity) {               \
    if (!pool || capacity == 0) return NX_ERR_INVALID_ARGS;                         \
    pool->data = (T*)malloc(capacity * sizeof(T));                                  \
    pool->generation = (uint32_t*)calloc(capacity, sizeof(uint32_t));               \
    pool->active = (bool*)calloc(capacity, sizeof(bool));                           \
    pool->free_list = (uint32_t*)malloc(capacity * sizeof(uint32_t));               \
    if (!pool->data || !pool->generation || !pool->active || !pool->free_list) {    \
        free(pool->data);                                                           \
        free(pool->generation);                                                     \
        free(pool->active);                                                         \
        free(pool->free_list);                                                      \
        return NX_ERR_NULLPTR;                                                      \
    }                                                                               \
    for (size_t i = 0; i < capacity; i++)                                           \
        pool->free_list[i] = (uint32_t)(capacity - 1 - i);                          \
    pool->capacity = capacity;                                                      \
    pool->free_count = capacity;                                                    \
    return NX_OKAY;                                                                 \
}                                                                                   \
\
static NxStatus NAME##_Pool_Grow(NAME##Pool* pool, size_t new_capacity) {           \
    if (!pool || new_capacity <= pool->capacity)                                    \
        return NX_ERR_INVALID_ARGS;                                                 \
    T* new_data = (T*)realloc(pool->data, new_capacity * sizeof(T));                \
    uint32_t* new_gen = (uint32_t*)realloc(                                         \
        pool->generation,                                                           \
        new_capacity * sizeof(uint32_t)                                             \
    );                                                                              \
    bool* new_active = (bool*)realloc(                                              \
        pool->active,                                                               \
        new_capacity * sizeof(bool)                                                 \
    );                                                                              \
    uint32_t* new_free = (uint32_t*)realloc(                                        \
        pool->free_list,                                                            \
        new_capacity * sizeof(uint32_t)                                             \
    );                                                                              \
    if (!new_data || !new_gen || !new_active || !new_free)                          \
        return NX_ERR_NULLPTR;                                                      \
    pool->data = new_data;                                                          \
    pool->generation = new_gen;                                                     \
    pool->active = new_active;                                                      \
    pool->free_list = new_free;                                                     \
    for (size_t i = pool->capacity; i < new_capacity; i++) {                        \
        pool->generation[i] = 0;                                                    \
        pool->active[i] = false;                                                    \
        pool->free_list[pool->free_count++] = (uint32_t)i;                          \
    }                                                                               \
    pool->capacity = new_capacity;                                                  \
    return NX_OKAY;                                                                 \
}                                                                                   \
\
static inline int32_t NAME##_Pool_Acquire(NAME##Pool* pool) {                       \
    if (!pool) return -1;                                                           \
    if (pool->free_count == 0) {                                                    \
        size_t new_cap = pool->capacity == 0 ? 1 : pool->capacity * 2;              \
        if (NAME##_Pool_Grow(pool, new_cap) != NX_OKAY) return -1;                  \
    }                                                                               \
    uint32_t idx = pool->free_list[--pool->free_count];                             \
    pool->active[idx] = true;                                                       \
    memset(&pool->data[idx], 0, sizeof(T));                                         \
    return (int32_t)idx;                                                            \
}                                                                                   \
\
static inline NxStatus NAME##_Pool_Release(NAME##Pool* pool, int32_t index) {       \
    if (!pool || index < 0 || (size_t)index >= pool->capacity)                      \
        return NX_ERR_INVALID_ARGS;                                                 \
    if (!pool->active[index]) return NX_ERR_INVALID_ARGS;                           \
    pool->active[index] = false;                                                    \
    pool->generation[index]++;                                                      \
    pool->free_list[pool->free_count++] = (uint32_t)index;                          \
    return NX_OKAY;                                                                 \
}                                                                                   \
\
static inline T* NAME##_Pool_Get(NAME##Pool* pool, int32_t index, uint32_t gen) {   \
    if (!pool || index < 0 || (size_t)index >= pool->capacity)                      \
        return NULL;                                                                \
    if (!pool->active[index] || pool->generation[index] != gen)                     \
        return NULL;                                                                \
    return &pool->data[index];                                                      \
}                                                                                   \
\
static inline uint32_t NAME##_Pool_GetGeneration(NAME##Pool* pool, int32_t index) { \
    if (!pool || index < 0 || (size_t)index >= pool->capacity)                      \
        return 0;                                                                   \
    return pool->generation[index];                                                 \
}                                                                                   \
\
static void NAME##_Pool_Destroy(NAME##Pool* pool) {                                 \
    if (!pool) return;                                                              \
    free(pool->data);                                                               \
    free(pool->generation);                                                         \
    free(pool->active);                                                             \
    free(pool->free_list);                                                          \
    memset(pool, 0, sizeof(NAME##Pool));                                            \
}

#endif
#ifndef TEXTURE_H
#define TEXTURE_H



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
#ifndef RECT_H
#define RECT_H 

typedef struct {
   float x, y, width, height;
} NxRect; 

#endif 



#ifndef VEC2_H
#define VEC2_H

typedef struct {
    float x, y;
} NxVector2; 

#endif
#ifndef COLOR_H
#define COLOR_H


typedef struct {
    uint8_t r; 
    uint8_t g;
    uint8_t b; 
    uint8_t a; 
} NxColor;  

#endif  

#ifndef RENDERER_H
#define RENDERER_H







typedef enum {
    NX_BLEND_ALPHA = 0,
    NX_BLEND_ADDITIVE,
    NX_BLEND_MULTIPLIED,
    NX_BLEND_ADD_COLORS
} NxBlend;

typedef struct {
    void (*init)(void);
    void (*beginFrame)(void);
    void (*endFrame)(void);
    void (*clear)(NxColor);
    void (*draw)(const NxTexture*, NxRect, NxRect, NxVector2, float, NxColor);
    void (*setBlend)(NxBlend);
} NxRendererDriver;

void Nx_RendererInit(const NxRendererDriver* driver);
void Nx_RendererBeginFrame(void);
void Nx_RendererEndFrame(void);
void Nx_RendererClear(NxColor color);
void Nx_RendererDraw(
    const NxTexture* texture,
    NxRect source, NxRect dest,       
    NxVector2 origin, float rotation, 
    NxColor tint
);
void Nx_RendererSetBlend(NxBlend blend);

#endif
#ifndef KEYBOARD_H
#define KEYBOARD_H

#ifndef I_KEY_H
#define I_KEY_H

typedef enum {
    NX_K_UNKNOWN = 0,
    NX_K_LEFT,
    NX_K_RIGHT,
    NX_K_UP,
    NX_K_DOWN,
    NX_K_A,
    NX_K_B,
    NX_K_C,
    NX_K_D,
    NX_K_E,
    NX_K_F,
    NX_K_G,
    NX_K_H,
    NX_K_I,
    NX_K_J,
    NX_K_K,
    NX_K_L,
    NX_K_M,
    NX_K_N,
    NX_K_O,
    NX_K_P,
    NX_K_Q,
    NX_K_R,
    NX_K_S,
    NX_K_T,
    NX_K_U,
    NX_K_V,
    NX_K_W,
    NX_K_X,
    NX_K_Y,
    NX_K_Z,
    NX_K_0,
    NX_K_1,
    NX_K_2,
    NX_K_3,
    NX_K_4,
    NX_K_5,
    NX_K_6,
    NX_K_7,
    NX_K_8,
    NX_K_9,
    NX_K_SPACE,
    NX_K_ENTER,
    NX_K_ESCAPE,
    NX_K_TAB,
    NX_K_BACKSPACE,
    NX_K_LEFT_SHIFT,
    NX_K_RIGHT_SHIFT,
    NX_K_LEFT_CONTROL,
    NX_K_RIGHT_CONTROL,
    NX_K_LEFT_ALT,
    NX_K_RIGHT_ALT,
    NX_KEY_NUMBER
} NxKey;

#endif 


typedef struct {
    bool (*keyPressed)(NxKey key);
    bool (*keyReleased)(NxKey key);
    bool (*keyActive)(NxKey key);
} NxKeyboardDriver;

void Nx_KeyboardInit(const NxKeyboardDriver* driver);

bool Nx_KeyPressed(NxKey key);
bool Nx_KeyActive(NxKey key);
bool Nx_KeyReleased(NxKey key);

#endif
#ifndef BACKEND_H
#define BACKEND_H





#ifndef TIME_BACK_H
#define TIME_BACK_H



typedef struct {
    int targetFps;
} NxTime;

typedef struct {
    float (*getDt)(void);
    int (*getFps)(void);
    void (*setTargetFps)(int);
} NxTimeDriver;

void Nx_TimeInit(const NxTimeDriver* driver, NxTime time);

float Nx_GetDt(void);
int Nx_GetFps(void);
void Nx_SetTargetFps(int targetFps);

#endif

#define N_BACKENDS 1

typedef enum {
    NX_BACKEND_RAYLIB = 0
} NxBackends;

typedef struct {
    NxWindowDriver* windowDriver;
    NxTextureDriver* textureDriver;
    NxRendererDriver* rendererDriver;
    NxKeyboardDriver* keyboardDriver;
    NxTimeDriver* timeDriver;
} NxBackend;

extern NxBackend backendTable[N_BACKENDS];

void Nx_RegisterBackends(void);

void Nx_Init(
    NxBackend backend,
    int virtualWidth, int virtualHeight,
    float scale_X, float scale_Y,
    bool vsync, int targetFps,
    const char* title
);

#endif


#endif