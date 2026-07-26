#ifndef MISC_H
#define MISC_H

#include "nodex/status/status.h"

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