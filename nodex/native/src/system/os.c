#include "nodex/system/os.h"

#define COLOR_RED "\033[31m"
#define COLOR_RESET "\033[0m"

void Os_Panic(const char* new_err_msg, const char* source) {
    fprintf(stderr, 
        COLOR_RED "\n===========================================================================\n"
        "                          [FATAL ENGINE PANIC]           \n"
        "  Uncontrolled error sequence detected in source: %s     \n"
        "  New error: %s                                          \n"
        "  Terminating process immediately to prevent corruption. \n"
        "===========================================================================\n" COLOR_RESET,
        source, new_err_msg
    );
    fflush(stderr);
    _Exit(EXIT_FAILURE);
}