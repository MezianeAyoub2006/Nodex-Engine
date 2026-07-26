#ifndef TIME_BACK_H
#define TIME_BACK_H

#include "nodex/status/status.h"

typedef struct {
    int targetFps;
} NxTime;

typedef struct {
    float (*getDt)(void);
    int (*getFps)(void);
    void (*setTargetFps)(int);
} NxTimeDriver;

void Nx_TimeInit(const NxTimeDriver* driver, NxTime time);

float Nx_GetDt(void);
int Nx_GetFps(void);
void Nx_SetTargetFps(int targetFps);

#endif