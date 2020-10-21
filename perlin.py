import numpy as np

import matplotlib.pyplot as plt

class Perlin:
    def __init__(self, n = 4, dt = 0.1):
        # lattice = int coordinates
        self.n = n # grid size
        self.dt = dt # min offset
        self.f = int(1/dt) # freq within lattice
        self.N = n * self.f

        self.lattice = []
        for x in range(n):
            l = []
            for y in range(n):
                theta = np.random.random() * 2* np.pi
                l += [(np.cos(theta), np.sin(theta))]
            self.lattice += [l]
        # print(f'lattice {self.lattice}')

        self.grid = []
        for x in np.arange(0,n,dt):
            l=[]
            for y in np.arange(0,n,dt):
                X = int(x)
                Y = int(y)
                X1 = (X + 1)%n
                Y1 = (Y+1)%n
                dx = x - X
                dy = y - Y

                dot00 = self.lattice[X][Y][0]*dx + self.lattice[X][Y][1]*dy
                dot10 = self.lattice[X1][Y][0]*(1-dx) + self.lattice[X1][Y][1]*dy
                dot01 = self.lattice[X][Y1][0]*dx + self.lattice[X][Y1][1]*(1-dy)
                dot11 = self.lattice[X1][Y1][0]*(1-dx) + self.lattice[X1][Y1][1]*(1-dy)

                l1 = self.lerp(dot00, dot10, dx)
                l2 = self.lerp(dot01, dot11, dx)

                y = self.cerp(l1,l2, dy)

                l += [y]
            self.grid += [l]

        
    def lerp(self, a,b,dx):
        return a*(1-dx) + b * dx

    def cerp(self, a,b,dx):
        t = (3 - 2 * dx) * dx * dx
        return a*(1-t) + b*t

    def get(self,x,y):
        X = int(x)
        Y = int(y)
        dx = x - X
        dy = y - Y
        X = X % self.n
        Y = Y % self.n

        x = f * (X+dx)
        y = f * (Y+dy)

        return self.grid[int(x)][int(y)]
    

