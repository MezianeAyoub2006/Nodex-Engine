#include "nodex/drivers/drivers.h"

float (*internal_get_dt)(void); 

void Nx_Dt_Init(float (*get_dt)(void)) {
    internal_get_dt = get_dt; 
}

float Nx_Get_Dt(void) {
    return internal_get_dt(); 
}
