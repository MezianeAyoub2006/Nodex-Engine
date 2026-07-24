#ifndef MISC_H
#define MISC_H

#include "nodex/status/status.h"

#define NX_CHECK_NULLSIZE(w, h) \
    do { \
        if ((w) <= 0 || (h) <= 0) \
            return NX_ERR_INVALID_ARGS; \
    } while (0) 

#endif 