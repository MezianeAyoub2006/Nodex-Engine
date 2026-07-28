import nodex 
import random
import time

W, H = 1280, 720

ctx = nodex.Context((W, H), (1, 1), True, 1000)  

tex = nodex.Texture("nodex.png")

@ctx.run()
def loop():
   ctx.wrapper.renderer.draw_fast(tex, nodex.Rect(0, 0, tex.width, tex.height), nodex.Color(255, 255, 255, 255), 0)