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