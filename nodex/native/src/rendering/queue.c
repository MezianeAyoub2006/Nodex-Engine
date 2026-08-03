#include <stdio.h>
#include "nodex/rendering/queue.h"
#include "nodex/drivers/renderer.h"

NxRenderingQueue queue; 

NxRenderingQueue* Nx_RenderingQueue_Get(void) {
    return &queue; 
}

void Nx_RenderingQueue_Update(void) {
    for (int i = 0; i < queue.count; i++) {
        NxRenderingTask task = queue.tasks[i]; 
        switch (task.type) {
            case TASK_SIMPLE: 
                NxTaskSimple s = task.simple; 
                Nx_Renderer_DrawSimple(
                    s.texture, 
                    (NxVec2){s.pos_x, s.pos_y}
                ); 
                break; 
            case TASK_NORMAL: 
                NxTaskNormal n = task.normal; 
                Nx_Renderer_Draw(
                    n.texture, 
                    (NxVec2){n.pos_x, n.pos_y}, 
                    n.rotation,
                    n.scale 
                ); 
                break; 
            case TASK_FULL: 
                NxTaskFull f = task.full; 
                Nx_Renderer_DrawFull(
                    f.texture, 
                    (NxRect){f.source_x, f.source_y, f.source_w, f.source_h}, 
                    (NxRect){f.dest_x, f.dest_y, f.dest_w, f.dest_h}, 
                    (NxVec2){f.origin_x, f.origin_y},
                    f.rotation,
                    (NxColor){f.tint_r, f.tint_g, f.tint_b, f.tint_a} 
                );
                break; 
        }
    }
    queue.count = 0;  
} 
