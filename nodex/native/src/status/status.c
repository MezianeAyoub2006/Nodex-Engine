#include "nodex/status/status.h" 
#include "nodex/system/os.h"

NxInterface_Status status_interface; 

void Nx_ThrowError(NxStatus error, const char* source, const char* message) {
    if (status_interface.error_happened) {
        Os_Panic(message, source);
        return; 
    }  
    status_interface.error_happened = true; 
    status_interface.error = (NxError){
        .message = message,
        .source = source,
        .type = error 
    };  
}

void Nx_ThrowWarning(NxStatus type, NxWarnPriority priority, const char* message) {
    if (status_interface.warnings_count >= 100) {
        Nx_ThrowError(
            NX_ERR_OVERFLOW, 
            "Nx_ThrowWarning",
            "Warnings array overflow." 
        ); 
        return; 
    }
    status_interface.warnings[status_interface.warnings_count++] = (NxWarning){
        .message = message,
        .priority = priority,
        .type = type 
    };
}

NxInterface_Status* NxInterface_Status_Get(void) { 
    return &status_interface; 
}
 
bool Nx_CheckError(void) {
    return status_interface.error_happened;  
} 
