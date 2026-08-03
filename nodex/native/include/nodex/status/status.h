#pragma once 

#include <stdint.h>
#include <stdbool.h>

#include "nodex/status/macros.h"

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


