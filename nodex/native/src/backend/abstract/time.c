#include <stdlib.h>
#include "nodex/backend/abstract/time.h"
#include "nodex/macros/misc.h"

static NxTime time;
static const NxTimeDriver* timeDriver = NULL;

void Nx_TimeInit(const NxTimeDriver* driver, NxTime ex_time) {
    NX_CHECK_DRIVER(driver, );

    if (ex_time.targetFps <= 1) {
        Nx_SetStatus(NX_ERR_INVALID_ARGS, "Target FPS must be greater than 1");
        return;
    }

    time = ex_time;
    timeDriver = driver;
}

float Nx_GetDt(void) {
    NX_DRIVER_DISPATCH(timeDriver, getDt, -1.0f);
}

int Nx_GetFps(void) {
    NX_DRIVER_DISPATCH(timeDriver, getFps, -1);
}

void Nx_SetTargetFps(int target_fps) {
    if (target_fps <= 1) {
        Nx_SetStatus(NX_ERR_INVALID_ARGS, "Target FPS must be greater than 1");
        return;
    }

    time.targetFps = target_fps;

    NX_DRIVER_DISPATCH_VOID(timeDriver, setTargetFps, target_fps);
}