import copy
import matplotlib.pyplot as plt
from matplotlib import animation, rc
from IPython.display import HTML
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import pandas as pd
import math

Gconst = 6.67408e-11
#Gconst = 5.76288e-7
#Gconst = 1
class GravitationalObject:
    def __init__(self, x0, y0, vx0, vy0, mass, size = 1, color='skyblue'):
        self.x = x0
        self.y = y0
        self.vx = vx0
        self.vy = vy0
        self.mass = mass
        self.size = size
        self.color=color
    
    def __str__ (self):
        return 'GravitationalObject(x=' + str(self.x) + ', y=' + str(self.y) + ', vx=' + str(self.vx) + ', vy=' + str(self.vy) + ', mass=' + str(self.mass) + ')\n'
    
    def __repr__(self):
        return str(self)

    def acceleration_from_other_object(self, other):
        acc_x = 0
        acc_y = 0
        dx = abs(self.x-other.x)
        dy = abs(self.y-other.y)
        r = (math.sqrt(dx**2 + dy**2))
        force = Gconst*self.mass*other.mass/r**2
        # Compute the direction of the force.
        fx =force * dx/r
        fy =force * dy/r
        acc_x = fx/self.mass #* ((24*3600)**2)/1000
        acc_y = fy/self.mass #* ((24*3600)**2)/1000
        if (other.x <= self.x):
            acc_x = -acc_x
        if (other.y <= self.y):
            acc_y = -acc_y
    
        # if(self.x != other.x):
        #     force_x = Gconst*self.mass*other.mass/((abs(self.x-other.x))**2)
        #     acc_x = force_x/self.mass
        #     if (other.x <= self.x) and (self.vx >= 0):
        #         acc_x = -acc_x
        # if(self.y != other.y):
        #     force_y = Gconst*self.mass*other.mass/((abs(self.y-other.y))**2)
        #     acc_y = force_y/self.mass
        #     if (other.y <= self.y) and (self.vy >= 0):
        #         acc_y = -acc_y
        return [acc_x, acc_y]

    def move_a_tick(self, accelerations, tick=1):
        self.x = self.x + self.vx * tick + accelerations[0] * tick**2 / 2
        self.y = self.y + self.vy * tick  + accelerations[1] * tick**2 / 2
        self.vx = self.vx + accelerations[0] * tick
        self.vy = self.vy + accelerations[1] * tick

class GravityField:
    def __init__(self):
        self.objects = []
        self.history = []

    def __str__(self):
        res = ''
        for i in self.objects:
            res = res + str(i)
            res = res + "\n"
        return res

    def add_body(self, body):
        self.objects.append(body)

    def tick(self):
        #save history for visualization
        self.history.append(copy.deepcopy(self.objects))

        #calculate accelerations of objects
        objects_acc = []
        for i in self.objects:
            acc = [0, 0]
            for j in self.objects:
                if (j!=i):
                    accelerations = i.acceleration_from_other_object(j)
                    acc[0] = acc[0] + accelerations[0]
                    acc[1] = acc[1] + accelerations[1]                    
            objects_acc.append(acc)

        #calculate new positions of objects: tick means t = 1
        t = 3600*24
        for x, obj in enumerate(self.objects):
            obj.move_a_tick(objects_acc[x], t)

    def simulate_n_ticks(self, n=10):
        for i in range(n):
            self.tick()

    def animate(self, i, arg):
        arg.clf()
        plt.axis([-1.65e11, 1.65e11, -1.65e11, 1.65e11])
        for obj in self.history[i]:
            p = plt.scatter(obj.x, obj.y, color=obj.color, s = obj.size)
            

print("Gravitational field simulation")
#Sun at center of galaxy
obj = GravitationalObject(0.0, 0.0, 0.0, 0.0, 1.989e30, 500, 'yellow')
#Earth at 1 AU from Sun
obj2 = GravitationalObject(0.0, 149597870000, 30000, 0.0, 5.97e24, 50, 'skyblue')
#Moon
obj3 = GravitationalObject(0.0, 149597870000+384399000, 30000+1023,0.0, 7.347673e22, 10, 'grey')
#obj = GravitationalObject(100, 100, 10, -10, 500)
#obj2 = GravitationalObject(-100, -40, -10, 10, 1000)
#obj3 = GravitationalObject(0, 0, 0, 0, 80000)
field = GravityField()
field.add_body(obj)
field.add_body(obj2)
field.add_body(obj3)
print(field)
field.simulate_n_ticks(360)
fig = plt.figure()

plt.axis([-1.65e11, 1.65e11, -1.65e11, 1.65e11])
plt.style.use('dark_background')
animator = animation.FuncAnimation(fig, field.animate,  fargs=(fig,))
plt.show()
print(field.history)
