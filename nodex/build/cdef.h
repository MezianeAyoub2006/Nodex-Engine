/* Custom definitions to the pipeline */

typedef unsigned char uint8_t;

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
    FLAG_VSYNC_HINT = 0x00000040,
    FLAG_WINDOW_HIDDEN = 0x00000080,
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
/*Checks if a status is a warning.
[ Examples ]
NX_IS_WARNING(NX_WARN) -> 1
NX_IS_WARNING(NX_ERR_OUT_OF_MEMORY) ->  0
NX_IS_WARNING(NX_OKAY) -> 0*/
/* Sets the global status of the engine execution */
void Nx_SetStatus(NxStatus status, const char* message);
/* Retrieves the last status set by Nx_SetStatus. */
NxStatus Nx_GetStatus(void);
/* Retrieves the message tied to the last status set by Nx_SetStatus. */
const char* Nx_GetStatusMessage(void);
/* Checks if (w, h) surface has negative size */
/* Checks if a specified driver is valid */
/* Checks if a feature if implemented */
/* Dispach a function into a driver, forwarding its return value */
/* Dispatch a function into a driver, without forwarding a value (void callers) */
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
    bool (*shouldClose)(void);
} NxWindowDriver;
const NxWindow* Nx_WindowGet(void);
void Nx_WindowInit(const NxWindowDriver* driver, NxWindow window);
void Nx_WindowSetVirtualSize(int virtualWidth, int virtualHeight);
void Nx_WindowSetScale(float scale_X, float scale_Y);
void Nx_WindowSetTitle(const char* title);
void Nx_WindowToggleFullscreen(void);
bool Nx_WindowShoudClose(void);
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
typedef struct {
   float x, y, width, height;
} NxRect; 
typedef struct {
    float x, y;
} NxVector2; 
typedef struct {
    uint8_t r; 
    uint8_t g;
    uint8_t b; 
    uint8_t a; 
} NxColor;  
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
    void (*drawFast)(const NxTexture*, NxRect, NxColor); 
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
void Nx_RendererDrawFast(
    const NxTexture* texture,
    NxRect dest,        
    NxColor tint
);
void Nx_RendererSetBlend(NxBlend blend);
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
typedef struct {
    bool (*keyPressed)(NxKey key);
    bool (*keyReleased)(NxKey key);
    bool (*keyActive)(NxKey key);
} NxKeyboardDriver;
void Nx_KeyboardInit(const NxKeyboardDriver* driver);
bool Nx_KeyPressed(NxKey key);
bool Nx_KeyActive(NxKey key);
bool Nx_KeyReleased(NxKey key);
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
NxBackend* Nx_GetBackendTable(void); 
void Nx_RegisterBackends(void);
void Nx_Init(
    NxBackend backend,
    int virtualWidth, int virtualHeight,
    float scale_X, float scale_Y,
    bool vsync, int targetFps,
    const char* title
);
// wierd guard name cause scared of wierd shi.
typedef struct {
    NxTexture* texture;   
    NxRect source;        
    NxRect dest;          
    NxVector2 origin;     
    float rotation;       
    float z_index;
    NxColor tint;         
    int arrival_id;       
} NxDrawTask;
typedef struct { 
    NxDrawTask drawTasks[20000]; 
    int ptr; 
} NxDrawQueue;
typedef struct {
    NxTexture* texture;
    NxRect dest; 
    float z_index; 
    int arrival_id; 
    NxColor tint; 
} NxDrawTaskFast; 
typedef struct {
    NxDrawTaskFast drawTasks[20000]; 
    int ptr; 
} NxDrawQueueFast; 
typedef struct {
    bool active[NX_KEY_NUMBER]; 
    bool pressed[NX_KEY_NUMBER]; 
    bool released[NX_KEY_NUMBER]; 
} NxKeyboardState; 
typedef struct {
    bool shouldClose;   
    int fps; 
    float dt;  
    NxDrawQueue drawQueue;  
    NxDrawQueueFast drawQueueFast; 
    NxKeyboardState keyboardState; 
    // inserer interface pour python ici
} NxInterface;
NxInterface* Nx_GetInterface(void);
void Nx_Update(void);