#pragma once

#define _ERROR_BODY(error_type, message)                                        \
Nx_ThrowError(                                                                  \
    (error_type),                                                               \
    __func__,                                                                   \
    message                                                                     \
);     

#define NX_NONE(...) \ ((void)0)

#define NX_ERROR_IF(condition, error_type, message, action)                     \
    do {                                                                        \
        if ((condition)) {                                                      \
            _ERROR_BODY(error_type, message);                                   \
            do {action;} while (0);                                             \
        }                                                                       \
    } while (0) 

#define NX_WARNING_IF(condition, warn_type, priority, message)                  \
do {                                                                            \
    if ((condition)) {                                                          \
        Nx_ThrowWarning(                                                        \
            (warn_type),                                                        \
            (priority),                                                         \
            message                                                             \
        );                                                                      \
    }                                                                           \
} while (0)          

#define NX_CHECK(...)                                                           \
    do {                                                                        \
        if (Nx_CheckError()) {                                                  \
            return __VA_ARGS__;                                                 \
        }                                                                       \
    } while (0)

#ifdef NX_PERF
    #define NX_ERROR_IF_PERF(condition, error_type, message, action) NX_NONE()         
#else
    #define NX_ERROR_IF_PERF(condition, error_type, message, action)            \
        NX_ERROR_IF(condition, error_type, message, action)
#endif

#ifdef NX_DEBUG
    #define NX_CHECK_DEBUG(...)                                                 \
    do {                                                                        \
        NX_CHECK(__VA_ARGS__);                                                  \
    } while (0)
#else
    #define NX_CHECK_DEBUG(...) NX_NONE()
#endif


