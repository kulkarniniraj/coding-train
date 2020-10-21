import numpy as np
from perlin import Perlin
import pygame
import time

def mymap(x, r1, r2, s1, s2):
    '''
    Maps x in range (r1, r2) to (s1, s2)
    '''
    rs = r2-r1
    ss = s2-s1
    return (x-r1) * ss / rs + s1

n = 5
dt = 0.2
f = int(1/dt)
N = int(n/dt)

def idx(x,z):
    return x*N + z

def tfm_points(pts):
    '''
    transform vertices from 3d to 2d
    '''
    # perspective transform
    tfm = pts * znear / pts[:, 2:] 
    tfm += 0.5

    colors = np.zeros_like(tfm)
    
    # move to screen coordinates
    tfm[:,0] *= 1600
    tfm[:,1] *= 900

    # define colors according to y and z
    r = 900 - tfm[:, 1]
    r = (r - r.min()) / (r.max() - r.min())

    g = pts[:, 2]
    g = (g - g.min()) / (g.max() - g.min())
    g = 1 - g

    b = pts[:, 2]
    b = (b - b.min()) / (b.max() - b.min())

    colors[:, 0] = r
    colors[:, 1] = g
    colors[:, 2] = b
    return tfm, colors

def gen_points():
    '''
    generate initial mesh points
    '''
    pts = np.zeros((N * N, 3))
    pts[:, 0] = np.repeat(np.arange(-N/2,N/2), N)
    pts[:, 2] = np.tile(np.arange(N) + 10, N)
    p1 = Perlin(n, dt)
    Y = np.array(p1.grid).ravel()
    Y /= Y.max()
    return pts, Y

znear = 1
pts, Y = gen_points()

pygame.init()

primary = pygame.display.set_mode()
running = True
while running:
    # clear screen
    primary.fill((0,0,0))

    # roll mesh height
    Y = np.roll(Y, -1)
    pts[:, 1] = 5 - 2*Y

    tfm, colors = tfm_points(pts)

    # draw mesh
    for x in range(N-1):
        for z in range(N-1):
            color = (colors[[idx(x,z), idx(x+1,z), idx(x+1, z+1)]].max(axis=0)*255).astype(int)
            pygame.draw.polygon(primary, tuple(color), tfm[[idx(x,z), idx(x+1,z), idx(x+1, z+1)], :2], 1) 

            color = (colors[[idx(x,z), idx(x+1,z+1), idx(x, z+1)]].max(axis=0)*255).astype(int)
            pygame.draw.polygon(primary, tuple(color), tfm[[idx(x,z), idx(x+1,z+1), idx(x, z+1)], :2], 1) 
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False
    time.sleep(0.04)
