# script used to convert a 3D Voxel Art slices spritesheet, to a billboard one

import pygame

pygame.init()
pygame.display.set_mode((1, 1), pygame.NOFRAME)

def spritestack(slices, angle, z_step=1):
    cx, cy = 0, 0
    rotated_slices = [pygame.transform.rotate(spr, angle) for spr in slices]

    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')

    positions = []
    for i, rot in enumerate(rotated_slices):
        rot_w, rot_h = rot.get_size()
        base_x = cx - rot_w // 2
        base_y = cy - rot_h // 2
        x = base_x
        y = base_y - i * z_step
        positions.append((x, y))
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x + rot_w)
        max_y = max(max_y, y + rot_h)

    surface_w = int(max_x - min_x)
    surface_h = int(max_y - min_y)
    surface = pygame.Surface((surface_w, surface_h), pygame.SRCALPHA)
    surface.fill((0, 0, 0, 0))

    for i, rot in enumerate(rotated_slices):
        x = int(positions[i][0] - min_x)
        y = int(positions[i][1] - min_y)
        surface.blit(rot, (x, y))

    return surface

INPUT      = "tree.png"
SIZE       = (100, 100)
ANGLE_STEP = 5
Z_STEP     = 1
OUTPUT     = "result.png"
SCALE = 2


slices_surface = pygame.image.load(INPUT).convert_alpha()
w, h = slices_surface.get_size()

slices = []
for y in reversed(range(h // SIZE[1])):
    slices.append(slices_surface.subsurface((0, y * SIZE[1], *SIZE)))


angles = list(range(0, 360, ANGLE_STEP))
frames = [spritestack(slices, a, Z_STEP) for a in angles]

if SCALE != 1:
    frames = [pygame.transform.scale(f, (f.get_width() * SCALE, f.get_height() * SCALE)) for f in frames]

frames = frames[::-1]

frame_w = max(f.get_width() for f in frames)
frame_h = max(f.get_height() for f in frames)

sheet = pygame.Surface((frame_w * len(frames), frame_h), pygame.SRCALPHA)
sheet.fill((0, 0, 0, 0))

for i, frame in enumerate(frames):
    x = i * frame_w + (frame_w - frame.get_width()) // 2
    y = (frame_h - frame.get_height()) // 2
    sheet.blit(frame, (x, y))

pygame.image.save(sheet, OUTPUT)
print(f"{frame_w}x{frame_h}")

pygame.quit()