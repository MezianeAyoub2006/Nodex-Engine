#ifndef MISC_H
#define MISC_H

#include "nodex/status/status.h"

/* Checks if (w, h) surface has negative size */
#define NX_CHECK_NEGSIZE(w, h)                                  \
    do {                                                        \
        if ((w) <= 0 || (h) <= 0)                               \
            return NX_ERR_INVALID_ARGS;                         \
    } while (0)                                

/* Checks if a specified driver is valid */
#define NX_CHECK_DRIVER(driver) \
    do {                                                        \
        if (!(driver))                                          \
            return NX_ERR_DRIVER_NULL;                          \
    } while (0) 

/* Checks if a feature if implemented */
#define NX_CHECK_FEATURE(func_ptr)                              \
    do {                                                        \
        if (!(func_ptr))                                        \
            return NX_WARN_FEATURE_NOT_SUPPORTED;               \
    } while (0)

/* Dispach a function into a driver */
#define NX_DRIVER_DISPATCH(driver, fn_name, ...)                \
    do {                                                        \
        NX_CHECK_DRIVER(driver);                                \
        NX_CHECK_FEATURE((driver)->fn_name);                    \
        return (driver)->fn_name(__VA_ARGS__);                  \
    } while (0)

#endif 