import pygame
import math
import random
import time

STATE = []

def mymap(x, r1, r2, s1, s2):
    """
    Map x from range (r1, r2) to (s1, s2)
    """
    rs = r2 - r1
    ss = s2 - s1
    return (x - r1)/rs * ss + s1

def draw(dt):
    """
    Pop a point and vector from STATE and draw a line.
    Insert two new points with random angle and reduced radius
    """
    start, radius, theta, w = STATE.pop() # w is line(branch) width
    if radius < 2:
        return
    dx = radius * math.sin(theta)
    dy = radius * math.cos(theta)
    end = (start[0] + dx, start[1] - dy)
    pygame.draw.line(primary, (mymap(w, 20, 0, 100, 60), mymap(w, 20, 0, 50, 155), 20), 
            start, end, int(w))
    pygame.display.update()
    STATE.append((end, radius*0.7, theta+dt+random.normalvariate(0, 3.14)/15, w-2))
    STATE.append((end, radius*0.7, theta-dt+random.normalvariate(0, 3.14)/15, w-2))

pygame.init()

primary = pygame.display.set_mode()

X = 750
Y = 800

dt = 3.14/6 # 30 degree default branch angle

STATE.append(((X,Y), 250, 0, 20)) # starting(root) point

while STATE:
    draw(dt)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            running = False

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                running = False
