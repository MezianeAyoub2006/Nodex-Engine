#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "nodex/status/format.h"
#include "nodex/status/status.h"

static const char* statusFormatTable[NX_STATUS_NUMBER] = {
    [NX_OKAY] = "SUCCESS",
    [NX_ERR] = "UNKNOWN",
    [NX_ERR_NULLPTR] = "NULL POINTER",
    [NX_ERR_INVALID_DRIVER_INIT] = "INVALID DRIVER INIT FUNCTION",
    [NX_ERR_DRIVER_NULL] = "INVALID DRIVER",
    [NX_ERR_INVALID_ARGS] = "INVALID FUNCTION ARGUMENTS",
    [NX_ERR_OUT_OF_MEMORY] = "OUT OF MEMORY",
    [NX_WARN] = "UNKNOWN",
    [NX_WARN_FEATURE_NOT_SUPPORTED] = "FEATURE NOT SUPPORTED"
};

bool Nx_FormatStatus(char* buff_out, size_t buff_size, NxStatus status) {
    if (buff_out == NULL) {
        Nx_SetStatus(NX_ERR_NULLPTR, "Output buffer is NULL");
        return false;
    }

    if (buff_size == 0) {
        Nx_SetStatus(NX_ERR_INVALID_ARGS, "Output buffer size is zero");
        return false;
    }

    if (status < 0 || status >= NX_STATUS_NUMBER) {
        Nx_SetStatus(NX_ERR_INVALID_ARGS, "Invalid status code");
        return false;
    }

    const char* msg = statusFormatTable[status];
    size_t msg_len = strlen(msg);

    if (msg_len >= buff_size) {
        memcpy(buff_out, msg, buff_size - 1);
        buff_out[buff_size - 1] = '\0';
        Nx_SetStatus(NX_WARN_FEATURE_NOT_SUPPORTED, "Buffer too small, message truncated");
        return false;
    }

    memcpy(buff_out, msg, msg_len + 1);
    return true;
}