#pragma once 

#include "nodex/drivers/renderer.h"
#include "nodex/drivers/texture.h"
#include "nodex/drivers/window.h"
#include "nodex/drivers/ray/ray.h"

void Nx_Dt_Init(float (*get_dt)(void));
float Nx_Get_Dt(void); 
