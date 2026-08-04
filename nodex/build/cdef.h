/* Custom definitions to the pipeline */

typedef unsigned char uint8_t;
typedef unsigned int uint32_t;
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
typedef enum {
    NX_PRIORITY_MIN,
    NX_PRIORITY_LOW,
    NX_PRIORITY_MIDLOW,
    NX_PRIORITY_MID,
    NX_PRIORITY_MIDHIGH,
    NX_PRIORITY_HIGH,
    NX_PRIORITY_MAX,
    NX_PRIORITY_COUNT  
} NxWarnPriority; 
typedef enum {
    NX_OKAY,
    NX_WARN,                    
    NX_WARN_NOT_IMPLEMENTED,    
    NX_WARN_REDEFINITION,
    NX_WARN_TIMING,
    NX_ERR, 
    NX_ERR_REDEFINITION, 
    NX_ERR_NULLPTR,
    NX_ERR_ARGS, 
    NX_ERR_OVERFLOW, 
    NX_ERR_OUT_OF_MEMORY, 
    NX_ERR_PREPROCESS,
    NX_STATUS_COUNT
} NxStatus; 
typedef struct {
    NxStatus type; 
    const char* message; 
    const char* source;  
} NxError;   
typedef struct { 
    NxStatus type;
    NxWarnPriority priority; 
    const char* message;  
} NxWarning; 
typedef struct {
    bool error_happened; 
    NxError error;
    NxWarning warnings[100];
    uint32_t warnings_count;  
} NxInterface_Status;
void Nx_ThrowError(NxStatus error, const char* source, const char* message); 
void Nx_ThrowWarning(NxStatus warning, NxWarnPriority priority, const char* message);  
bool Nx_CheckError(void); 
NxInterface_Status* NxInterface_Status_Get(void); 
typedef struct {
    float x; 
    float y;
} NxVec2;
typedef struct {
    uint8_t r; 
    uint8_t g; 
    uint8_t b;
    uint8_t a; 
} NxColor;
typedef struct {
    float x;
    float y; 
    float w; 
    float h; 
} NxRect; 
typedef enum {
    NX_DRIVER_RENDERER, 
    NX_DRIVER_TEXTURE,
    NX_DRIVER_WINDOW,
    NX_DRIVER_KEYBOARD 
} NxDriverType; 
typedef struct {
    void* raw; 
    NxVec2 size; 
} NxTexture; 
typedef struct {      
    NxDriverType type;   
    NxTexture* (*load)(const char*); 
    void (*unload)(NxTexture*);  
} NxTextureDriver;  
void Nx_Texture_Init(NxTextureDriver* driver); 
NxTexture* Nx_Texture_Load(const char* path);  
void Nx_Texture_Unload(NxTexture* texture); 
typedef struct {
    NxDriverType type; 
    void (*begin_frame)(void);
    void (*end_frame)(void);  
    void (*clear)(NxColor); 
    void (*draw_simple)(
        NxTexture* texture, 
        NxVec2 position
    );
    void (*draw)(
        NxTexture* texture,
        NxVec2 position,  
        float rotation, 
        float scale
    ); 
    void (*draw_full)(
        NxTexture* texture,
        NxRect source, 
        NxRect dest, 
        NxVec2 origin, 
        float rotation, 
        NxColor tint 
    ); 
} NxRendererDriver; 
void Nx_Renderer_Init(const NxRendererDriver* driver);
void Nx_Renderer_BeginFrame(void); 
void Nx_Renderer_EndFrame(void); 
void Nx_Renderer_Clear(NxColor color); 
void Nx_Renderer_DrawSimple(
    NxTexture* texture, 
    NxVec2 position
);
void Nx_Renderer_Draw(
    NxTexture* texture,
    NxVec2 position,  
    float rotation, 
    float scale
); 
void Nx_Renderer_DrawFull(
    NxTexture* texture,
    NxRect source, 
    NxRect dest, 
    NxVec2 origin, 
    float rotation, 
    NxColor tint 
); 
typedef struct {
    NxVec2 virtual_size;    
    NxVec2 scale;
    int flags; 
    int target_fps; 
    const char* caption;
} NxWindow; 
typedef struct {
    NxDriverType type; 
    void (*init)(NxWindow*);   
    void (*set_virtual_size)(NxWindow*); 
    void (*set_scale)(NxWindow*); 
    void (*set_target_fps)(NxWindow*); 
    void (*set_caption)(NxWindow*); 
    void (*toggle_fullscreen)(NxWindow*); 
    bool (*should_close)(NxWindow*); 
} NxWindowDriver; 
const NxWindow* Nx_Window_Get(void);
void Nx_Window_Init(const NxWindowDriver* driver, NxWindow window); 
void Nx_Window_SetVirtualSize(NxVec2 virtual_size); 
void Nx_Window_SetScale(NxVec2 scale);
void Nx_Window_SetTargetFps(int target_fps);  
void Nx_Window_SetCaption(const char* caption); 
void Nx_ToggleFullscreen(void); 
bool Nx_Window_ShouldClose(void); 
typedef enum {
    NX_KEY_NULL,
    NX_KEY_ZERO,
    NX_KEY_ONE,
    NX_KEY_TWO,
    NX_KEY_THREE,
    NX_KEY_FOUR,
    NX_KEY_FIVE,
    NX_KEY_SIX,
    NX_KEY_SEVEN,
    NX_KEY_EIGHT,
    NX_KEY_NINE,
    NX_KEY_A,
    NX_KEY_B,
    NX_KEY_C,
    NX_KEY_D,
    NX_KEY_E,
    NX_KEY_F,
    NX_KEY_G,
    NX_KEY_H,
    NX_KEY_I,
    NX_KEY_J,
    NX_KEY_K,
    NX_KEY_L,
    NX_KEY_M,
    NX_KEY_N,
    NX_KEY_O,
    NX_KEY_P,
    NX_KEY_Q,
    NX_KEY_R,
    NX_KEY_S,
    NX_KEY_T,
    NX_KEY_U,
    NX_KEY_V,
    NX_KEY_W,
    NX_KEY_X,
    NX_KEY_Y,
    NX_KEY_Z,
    NX_KEY_UP,
    NX_KEY_DOWN,
    NX_KEY_LEFT,
    NX_KEY_RIGHT,
    NX_KEY_SPACE,
    NX_KEY_ENTER,
    NX_KEY_ESCAPE,
    NX_KEY_TAB,
    NX_KEY_BACKSPACE,
    NX_KEY_INSERT,
    NX_KEY_DELETE,
    NX_KEY_HOME,
    NX_KEY_END,
    NX_KEY_PAGE_UP,
    NX_KEY_PAGE_DOWN,
    NX_KEY_F1,
    NX_KEY_F2,
    NX_KEY_F3,
    NX_KEY_F4,
    NX_KEY_F5,
    NX_KEY_F6,
    NX_KEY_F7,
    NX_KEY_F8,
    NX_KEY_F9,
    NX_KEY_F10,
    NX_KEY_F11,
    NX_KEY_F12,
    NX_KEY_LEFT_SHIFT,
    NX_KEY_RIGHT_SHIFT,
    NX_KEY_LEFT_CONTROL,
    NX_KEY_RIGHT_CONTROL,
    NX_KEY_LEFT_ALT,
    NX_KEY_RIGHT_ALT,
    NX_KEY_LEFT_SUPER,
    NX_KEY_RIGHT_SUPER,
    NX_KEY_CAPS_LOCK,
    NX_KEY_SCROLL_LOCK,
    NX_KEY_NUM_LOCK,
    NX_KEY_APOSTROPHE,
    NX_KEY_COMMA,
    NX_KEY_MINUS,
    NX_KEY_PERIOD,
    NX_KEY_SLASH,
    NX_KEY_SEMICOLON,
    NX_KEY_EQUAL,
    NX_KEY_LEFT_BRACKET,
    NX_KEY_BACKSLASH,
    NX_KEY_RIGHT_BRACKET,
    NX_KEY_GRAVE,
    NX_KEY_NUMBER
} NxKey;
typedef struct NxKeyboardDriver {    
    NxDriverType type;
    bool (*get_pressed)(NxKey); 
    bool (*get_active)(NxKey); 
    bool (*get_released)(NxKey);  
} NxKeyboardDriver;   
void Nx_Keyboard_Init(const NxKeyboardDriver* driver); 
bool Nx_Keyboard_GetPressed(NxKey key); 
bool Nx_Keyboard_GetActive(NxKey key); 
bool Nx_Keyboard_GetReleased(NxKey key); 
const NxRendererDriver* Raylib_RendererDriver(void); 
const NxTextureDriver* Raylib_TextureDriver(void); 
const NxWindowDriver* Raylib_WindowDriver(void); 
const NxKeyboardDriver* Raylib_KeyboardDriver(void); 
float Raylib_Get_Dt(void); 
void Nx_Dt_Init(float (*get_dt)(void));
float Nx_Get_Dt(void); 
void Nx_Init(
    NxVec2 virtual_size, 
    NxVec2 scale, 
    int flags, 
    int target_fps, 
    const char* caption,
    const NxWindowDriver* window_driver,
    const NxRendererDriver* renderer_driver,  
    const NxTextureDriver* texture_driver,
    const NxKeyboardDriver* keyboard_driver, 
    float (*get_dt)(void)
);
void Nx_Update(void); 
typedef struct {
    NxTexture* texture;  
    float pos_x; 
    float pos_y; 
} NxTaskSimple;
typedef struct {
    NxTexture* texture;  
    float pos_x; 
    float pos_y; 
    float rotation;
    float scale; 
} NxTaskNormal;
typedef struct {
    NxTexture* texture;  
    float source_x; 
    float source_y; 
    float source_w; 
    float source_h; 
    float dest_x;
    float dest_y;
    float dest_w;
    float dest_h; 
    float origin_x; 
    float origin_y; 
    float rotation; 
    uint8_t tint_r; 
    uint8_t tint_g; 
    uint8_t tint_b; 
    uint8_t tint_a; 
} NxTaskFull;
typedef enum {
    TASK_NORMAL, 
    TASK_SIMPLE,
    TASK_FULL 
} NxTaskType; 
typedef struct {
    NxTaskType type;     
    union {
        NxTaskNormal normal; 
        NxTaskSimple simple;
        NxTaskFull full; 
    }; 
    int order; 
} NxRenderingTask;
typedef struct {
    NxRenderingTask tasks[10000];
    uint32_t count; 
} NxRenderingQueue;
NxRenderingQueue* Nx_RenderingQueue_Get(void);
void Nx_RenderingQueue_Update(void); 
typedef struct {
    float dt; 
    float fps; 
    float interval; 
    double timer; 
} NxInterface_Time; 
typedef struct {
    NxKey requested_keys[256]; 
    bool pressed_keys[256]; 
    bool active_keys[256]; 
    bool released_keys[256];
    uint32_t count; 
} NxInterface_Keyboard;
NxInterface_Keyboard* Nx_Interface_Keyboard_Get(void); 
void Nx_Interface_Keyboard_Update(void);
typedef struct {
    bool should_close; 
    NxWindow* window;
    NxInterface_Status* status; 
    NxRenderingQueue* rendering_queue;
    NxInterface_Keyboard* keyboard; 
    NxInterface_Time time;  
} NxInterface; 
void Nx_Interface_Init(void); 
void Nx_Interface_Update(void);
NxInterface* Nx_Interface_Get(void); 