#pragma once

#if defined(_WIN32) || defined(_WIN64) || defined(__CYGWIN__)
    #define NX_PLATFORM_WINDOWS 1
#elif defined(__linux__)
    #define NX_PLATFORM_LINUX 1
#elif defined(__APPLE__) && defined(__MACH__)
    #define NX_PLATFORM_MACOS 1
#endif
