#pragma once 

#include "nodex/status/status.h"

#ifdef NX_PERF
    #define FULL_DISPATCH(driver, driver_name, func, fallback, ...)                \
        do {                                                                       \
            return (driver)->func(__VA_ARGS__);                                    \
        } while (0) 
    
#else
   #define FULL_DISPATCH(driver, driver_name, func, fallback, ...)                 \
        do {                                                                       \
            NX_ERROR_IF(!(driver), NX_ERR_NULLPTR,                                 \
                driver_name " driver is not initialized.",                         \
                return (fallback));                                                \
            NX_ERROR_IF(!((driver)->func), NX_WARN_NOT_IMPLEMENTED,                \
                #func " is not implemented on current backend.",                   \
                return (fallback));                                                \
            return (driver)->func(__VA_ARGS__);                                    \
        } while (0) 
#endif 

#ifdef NX_PERF
    #define FULL_DISPATCH_VOID(driver, driver_name, func, ...)                     \
        do {                                                                       \
            (driver)->func(__VA_ARGS__);                                           \
        } while (0)
#else
    #define FULL_DISPATCH_VOID(driver, driver_name, func, ...)                     \
        do {                                                                       \
            NX_ERROR_IF(!(driver), NX_ERR_NULLPTR,                                 \
                driver_name " driver is not initialized.",                         \
                return);                                                           \
            NX_ERROR_IF(!((driver)->func), NX_WARN_NOT_IMPLEMENTED,                \
                #func " is not implemented on current backend.",                   \
                return);                                                           \
            (driver)->func(__VA_ARGS__);                                           \
        } while (0)
#endif                                       

#define _CHECK_DRIVER_TYPE(driver, enum_type, serial_type, ...)                     \
    NX_ERROR_IF(                                                                    \
        (driver)->type != enum_type,                                                \
        NX_ERR_ARGS,                                                                \
        "Expected a " #serial_type " driver, got another kind.",                    \
        return __VA_ARGS__)

#define _CHECK_DRIVER_REDEFINITION(driver, driver_name, ...) \
    NX_ERROR_IF((driver) != NULL, NX_ERR_REDEFINITION, \
        "Redefining " #driver_name " driver while one was already registered.",\
        return __VA_ARGS__);

#define NX_DRIVER_CHECK(driver, static_driver, enum_type, serial_type, driver_name, ...)    \
do {                                                                                        \
    NX_REQUIRE_NONNULL(driver, serial_type);                                                \
    _CHECK_DRIVER_TYPE(driver, enum_type, serial_type, __VA_ARGS__);                        \
    _CHECK_DRIVER_REDEFINITION(static_driver, driver_name, __VA_ARGS__);                    \
} while (0)                                                                                  


