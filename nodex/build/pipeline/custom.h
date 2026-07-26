/* Custom definitions def to the pipeline */

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
