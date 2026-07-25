#ifdef __INTELLISENSE__ 
#include <stdint.h>
#endif

#define END_PREPROCESSOR


typedef enum {
    LOG_ALL = 0,        
    LOG_TRACE,          
    LOG_DEBUG,          
    LOG_INFO,           
    LOG_WARNING,        
    LOG_ERROR,          
    LOG_FATAL,          
    LOG_NONE            
} TraceLogLevel;

typedef struct Color { 
    unsigned char r, g, b, a; 
} Color;

typedef enum {
    FLAG_VSYNC_HINT         = 0x00000040,
    FLAG_WINDOW_HIDDEN      = 0x00000080,
} ConfigFlags;

typedef struct Texture {
    unsigned int id;
    int width;
    int height;
    int mipmaps;
    int format;
} Texture;


typedef Texture Texture2D;

void SetConfigFlags(unsigned int flags);
void ClearWindowState(unsigned int flags);
void SetTraceLogLevel(int logLevel);  
void InitWindow(int width, int height, const char *title);  
bool WindowShouldClose(void);
void CloseWindow(void);
void BeginDrawing(void);
void EndDrawing(void);
void ClearBackground(Color color);
void DrawTexture(Texture2D texture, int posX, int posY, Color tint);      

typedef struct Vector2 {
    float x;                
    float y;
} Vector2;

/*#########
## NODEX ##
#########*/

typedef enum {
    NX_OKAY = 0,                    
    NX_ERR,                         
    NX_ERR_NULLPTR,                 
    NX_ERR_INVALID_DRIVER_INIT,     
    NX_ERR_DRIVER_NULL,               
    NX_ERR_INVALID_ARGS,            
    NX_ERR_OUT_OF_MEMORY,           
    NX_WARN,    
    NX_WARN_FEATURE_NOT_SUPPORTED   
} NxStatus;

typedef enum {
    NX_BLEND_ALPHA = 0,
    NX_BLEND_ADDITIVE,
    NX_BLEND_MULTIPLIED,
    NX_BLEND_ADD_COLORS
} NxBlend;


typedef struct {
    uint8_t r; 
    uint8_t g;
    uint8_t b; 
    uint8_t a; 
} NxColor;  

typedef struct {
   float x, y, width, height;
} NxRect; 


typedef struct {
    float x, y;
} NxVector2; 

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



typedef struct {
    NxStatus (*init)(void);  
    NxStatus (*beginFrame)(void);
    NxStatus (*endFrame)(void);
    NxStatus (*clear)(NxColor color);
    NxStatus (*draw)(
        const NxTexture* texture, 
        NxRect source, 
        NxRect dest, 
        NxVector2 origin, 
        float rotation, 
        NxColor tint
    );
    NxStatus (*setBlend)(NxBlend blend);
} NxRendererDriver;

NxStatus Nx_RendererInit(const NxRendererDriver* driver); 
NxStatus Nx_RendererBeginFrame(void); 
NxStatus Nx_RendererEndFrame(void); 
NxStatus Nx_RendererClear(NxColor color);
NxStatus Nx_RendererDraw(
    const NxTexture* texture, 
    NxRect source, 
    NxRect dest, 
    NxVector2 origin, 
    float rotation, 
    NxColor tint
); 
NxStatus Nx_RendererSetBlend(NxBlend blend); 

typedef struct { 
int virtualWidth; 
    int virtualHeight; 
    float scale_X;
    float scale_Y; 
    bool fullscreen;
    bool vsync; 
    const char* title; 
} NxWindow;

typedef struct {
NxStatus (*init)(NxWindow*);
NxStatus (*setVirtualSize)(NxWindow*);
NxStatus (*setScale)(NxWindow*);
NxStatus (*setTitle)(NxWindow*);
NxStatus (*toggleFullscreen)(NxWindow*);
} NxWindowDriver;

const NxWindow* Nx_WindowGet(void); 
NxStatus Nx_WindowInit(const NxWindowDriver* driver, NxWindow window); 
NxStatus Nx_WindowSetVirtualSize(int virtualWidth, int virtualHeight); 
NxStatus Nx_WindowSetScale(float scale_X, float scale_Y); 
NxStatus Nx_WindowSetTitle(const char* title);
NxStatus Nx_WindowToggleFullscreen(void);

const NxRendererDriver* Nx_GetRaylibRendererDriver(void);
const NxTextureDriver* Nx_GetRaylibTextureDriver(void); 
const NxWindowDriver* Nx_GetRaylibWindowDriver(void);


typedef enum {
    NX_BACKEND_RAYLIB = 0 
} NxBackends; 

typedef struct {
    NxWindowDriver* windowDriver;
    NxTextureDriver* textureDriver; 
    NxRendererDriver* rendererDriver; 
} NxBackend; 

extern NxBackend backendTable[1];

void Nx_RegisterBackends(void);

NxStatus Nx_Init(
    NxBackend backend,
    int virtualWidth, 
    int virtualHeight,
    float scale_X,
    float scale_Y, 
    bool vsync, 
    const char* title
);