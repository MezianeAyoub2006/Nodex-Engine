#include <stddef.h>
#include "nodex/status/status.h"

static NxStatus lastStatus = NX_OKAY;
static const char* lastMessage = NULL;

void Nx_SetStatus(NxStatus status, const char* message) {
    lastStatus = status;
    lastMessage = message;
}

NxStatus Nx_GetStatus(void) {
    return lastStatus;
}

const char* Nx_GetStatusMessage(void) {
    return lastMessage;
}