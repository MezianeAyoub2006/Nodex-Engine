#include <stdio.h>

#define NX_INTERFACE_FIELDS \
    NX_READ(int, a)         \
    NX_WRITE(float, b)

#define NX_READ(type, val) type val;
#define NX_WRITE(type, val)
typedef struct {
    NX_INTERFACE_FIELDS
} PyInterface_User_Read;
#undef NX_READ
#undef NX_WRITE

#define NX_READ(type, val)
#define NX_WRITE(type, val) type val;
typedef struct {
    NX_INTERFACE_FIELDS
} PyInterface_User_Write;
#undef NX_READ
#undef NX_WRITE