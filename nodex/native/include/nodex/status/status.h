#ifndef STATUS_H
#define STATUS_H

typedef enum {
    NX_OKAY = 0, // shi fine.

    /* --------------- ERRORS --------------- */

    NX_ERR_NULLPTR,             // shi obvious.
    NX_ERR_INVALID_INIT_DRIVER, // when an invalid driver is passed to a backend object initialisation function.
    NX_ERR_DRIVER_NULL,         // when a driver is not initialized.
    NX_ERR_INVALID_ARGS,        // shi obvious sqrt(sqrt(sqrt(sqrt(32)))). 

    NX_WARN,    

    NX_WARN_FEATURE_NOT_SUPPORTED // when a driver doesn't implement a feature.
} NxStatus;

#endif