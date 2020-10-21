import pygame
import numpy as np
import time

# lines: 0 left, 1 top, 2 right, 3 bottom

SIZE = 15 # mesh size
mesh = np.ones((SIZE,SIZE,4))
visited = np.zeros((SIZE, SIZE)) # keeps track of visited squares

def mymap(x, r1, r2, s1, s2):
    '''
    Maps x in range (r1, r2) to (s1, s2)
    '''
    rspan = r2 - r1
    sspan = s2 - s1
    return (x-r1)*sspan/rspan + s1

def neighbours(x,y):
    '''
    returns neighbours of square given by (x, y)
    '''
    out = []
    mask = 0
    if x > 0:
        mask |= 1
    if x < SIZE - 1:
        mask |= 2
    if y > 0:
        mask |= 4
    if y < SIZE - 1:
        mask |= 8

    out = (out + [(0, (x-1,y))]) if (mask & 1) else out
    out = (out + [(2, (x+1,y))]) if (mask & 2) else out
    out = (out + [(1, (x,y-1))]) if (mask & 4) else out
    out = (out + [(3, (x,y+1))]) if (mask & 8) else out
    return out

def show_mesh(t):
    '''
    Renders current state of mesh
    t is current rect being processed
    '''
    offset = (300,0)
    size = (H-50)//(SIZE)
    for x in range(SIZE):
        xoff = offset[0] + x * size
        for y in range(SIZE):
            yoff = offset[1] + y * size

            if visited[x,y] == 1:
                pygame.draw.rect(primary, (200, 100, 0), (xoff, yoff, size, size))
            if mesh[x,y,0] == 1:
                pygame.draw.line(primary, (0,255,0), (xoff, yoff), (xoff, yoff+size))
            if mesh[x,y,1] == 1:
                pygame.draw.line(primary, (0,255,0), (xoff, yoff), (xoff+size, yoff))
            if mesh[x,y,2] == 1:
                pygame.draw.line(primary, (0,255,0), (xoff+size, yoff), (xoff+size, yoff+size))
            if mesh[x,y,3] == 1:
                pygame.draw.line(primary, (0,255,0), (xoff, yoff+size), (xoff+size, yoff+size))

    xoff = offset[0] + t[0] * size
    yoff = offset[1] + t[1] * size
    pygame.draw.rect(primary, (200, 0, 100), (xoff, yoff, size, size))

# initialization
pygame.init()

primary = pygame.display.set_mode()
W, H = primary.get_size()
running = True

# add first node (top left) to stack
stack = [(-1, (0,0))]

# main loop
while running:
    if stack:
        # get new node and previously visited node, to find common boundry
        prev, node = stack[-1]
        stack = stack[:-1]
        if not visited[node]:
            visited[node] = 1
            if prev == 0:
                # previous is to right of current
                mesh[node[0], node[1], 2] = 0
                mesh[node[0] + 1, node[1], 0] = 0
            if prev == 1:
                # previous is to bottom of current
                mesh[node[0], node[1], 3] = 0
                mesh[node[0], node[1] + 1, 1] = 0
            if prev == 2:
                # previous is to left of current
                mesh[node[0], node[1], 0] = 0
                mesh[node[0] - 1, node[1], 2] = 0
            if prev == 3:
                # previous is to top of current
                mesh[node[0], node[1], 1] = 0
                mesh[node[0], node[1] - 1, 3] = 0

            nbrs = neighbours(*node)
            # randomly shuffle neighbours to get random mesh
            np.random.shuffle(nbrs)
            for i, n in nbrs:
                stack += [(i,n)]

            time.sleep(0.2)

    primary.fill((0,0,0))
    show_mesh(node)
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

