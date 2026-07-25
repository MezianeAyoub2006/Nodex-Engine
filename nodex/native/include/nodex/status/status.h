#ifndef STATUS_H
#define STATUS_H

/*##################################################
##      NxState is mainly a return value for      ##
##  functions to indicate to the engine the state ##
##   of their execution, if everything went okay, ##
##  you will get NX_OKAY, if the developper want  ##
##    to warn you about some shi, you will get    ##
##  NX_WARN_... if the function completly failed, ##
##          you will get NX_ERR_...               ##
##################################################*/

typedef enum {
    NX_OKAY = 0,                    // shi fine.

    NX_ERR,                         
    /* --------------- ERRORS --------------- */
    NX_ERR_NULLPTR,                 // shi obvious. (unexpected NULL pointer passed.). 
    NX_ERR_INVALID_DRIVER_INIT,     // Driver struct is invalid or incomplete during init.
    NX_ERR_DRIVER_NULL,             // Engine subsystem driver has not been set yet. Use Nx_Init.  
    NX_ERR_INVALID_ARGS,            // shi obvious sqrt(sqrt(sqrt(sqrt(32)))). 
    NX_ERR_OUT_OF_MEMORY,           // Why even explain ? malloc failed, weak ass ram.

    NX_WARN,    
    /* -------------- WARNINGS --------------- */
    NX_WARN_FEATURE_NOT_SUPPORTED   // When a driver doesn't implement a feature.
} NxStatus;

#endif 

