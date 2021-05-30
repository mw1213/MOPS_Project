import copy
import matplotlib.pyplot as plt
from matplotlib import animation
import math

Gconst = 6.67408e-11
#Gconst = 1
base_size = 5
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
        acc_x = fx/self.mass
        acc_y = fy/self.mass
        if (other.x <= self.x):
            acc_x = -acc_x
        if (other.y <= self.y):
            acc_y = -acc_y
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

        #calculate new positions of objects: tick means number of seconds
        t = 3600
        for x, obj in enumerate(self.objects):
            obj.move_a_tick(objects_acc[x], t)

    def simulate_n_ticks(self, n=10):
        for i in range(n):
            self.tick()

    def animate(self, i, arg):
        arg.clf()
        plt.axis([-maxlen, maxlen, -maxlen, maxlen])
        plt.title("Solar system simulation")

        #plot only history of objects per day for faster simuluaton drawing
        for obj in self.history[i*24]:
            p = plt.scatter(obj.x, obj.y, color=obj.color, s = obj.size)
            plt.legend(["Sun", "Mercury","Venus", "Earth", "Moon","Mars", "Jupiter", "Saturn", "Uranus", "Neptune"], loc = "upper right")
            

print("Gravitational field simulation")
#Sun at center of galaxy
Sun = GravitationalObject(0.0, 0.0, 0.0, 0.0, 1.989e30, base_size*50, 'yellow')
#Earth at 1 AU from Sun
Earth = GravitationalObject(0.0, 149597870000, 30000, 0.0, 5.97e24, base_size*2.61, 'royalblue')
#Moon
Moon = GravitationalObject(0.0, 149597870000+384259000, 30000+1023,0.0, 7.347673e22, base_size*0.71, 'white')

#Mercury 
Mercury = GravitationalObject(57.9e9,0.0,0.0,-47400,0.33e24,size=base_size,color='silver')
#Venus
Venus = GravitationalObject(0.0, -108.2e9, -35.0e3, 0.0, 4.87e24, size=base_size*2.48, color='slategray')

#Mars
Mars = GravitationalObject(-227.9e9, 0.0, 0.0, 24.1e3, mass=0.642e24, size=base_size*1.39, color='maroon')

#Jupiter
Jupiter = GravitationalObject(778.6e9,0.0,0.0,-13.1e3, mass=1898e24, size= base_size*29.3, color='tan')

#Saturn
Saturn = GravitationalObject(-1433.5e9, 0.0, 0.0, 9.7e3, mass=568e24, size=base_size*24.7, color='darkkhaki')

#Uranus
Uranus = GravitationalObject(0.0, 2872.5e9, 6.8e3, 0.0,  mass=86.8, size=base_size*10.48, color='mediumspringgreen')

#Neptune
Neptune = GravitationalObject(0.0, -4495.1e9, -5.4e3, 0.0, mass=102e24, size=base_size*10.15, color='cyan')
field = GravityField()
field.add_body(Sun)
field.add_body(Mercury)
field.add_body(Venus)
field.add_body(Earth)
field.add_body(Moon)
field.add_body(Mars)
field.add_body(Jupiter)
field.add_body(Saturn)
field.add_body(Uranus)
field.add_body(Neptune)
#simulate 1.2 year
# 360*24*1.2 = 10368
field.simulate_n_ticks((10368))
fig = plt.figure()
#fix boundaries of animation of simuleted env
#for inner circle
#maxlen = 250e9
#for whole system
maxlen = 50e11
plt.axis([-maxlen, maxlen, -maxlen, maxlen])
plt.title("Solar system simulation")
plt.style.use('dark_background')
animator = animation.FuncAnimation(fig, field.animate, frames=375, interval=2, fargs=(fig,), save_count=400)
writergif = animation.PillowWriter(fps=30)
animator.save('solarsystemanimation.gif', writergif)
#animator.save('solarsysteminnercicleanimation.gif', writergif)
plt.show()
