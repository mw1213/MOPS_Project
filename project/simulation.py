import copy

Gconst = 6.673*(10**-11)
#Gconst = 1
class GravitationalObject:
    def __init__(self, x0, y0, vx0, vy0, mass):
        self.x = x0
        self.y = y0
        self.vx = vx0
        self.vy = vy0
        self.mass = mass
    
    def __str__ (self):
        return 'GravitationalObject(x=' + str(self.x) + ', y=' + str(self.y) + ', vx=' + str(self.vx) + ', vy=' + str(self.vy) + ', mass=' + str(self.mass) + ')\n'
    
    def __repr__(self):
        return str(self)

    def acceleration_from_other_object(self, other):
        acc_x = 0
        acc_y = 0
        if(self.x != other.x):
            force_x = Gconst*self.mass*other.mass/(abs(self.x-other.x))**2
            acc_x = force_x/self.mass
        if(self.y != other.y):
            force_y = Gconst*self.mass*other.mass/(abs(self.y-other.y))**2
            acc_y = force_y/self.mass
        return [acc_x, acc_y]

    def move_a_tick(self, accelerations, tick=1):
        self.x = self.x + self.vx * tick + accelerations[0] * tick**2 / 2
        self.y = self.y + self.vy * tick + accelerations[1] * tick**2 / 2
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
                    acc[0] = acc[0] - accelerations[0]
                    acc[1] = acc[1] - accelerations[1]                    
            objects_acc.append(acc)

        #calculate new positions of objects: tick means t = 1
        t = 1
        for x, obj in enumerate(self.objects):
            obj.move_a_tick(objects_acc[x], t)

    def simulate_n_ticks(self, n=10):
        for i in range(n):
            self.tick()




print("Gravitational field simulation")
#Sun at center of galaxy
obj = GravitationalObject(0.0, 0.0, 0.0, 0.0, 1.9885*10**33)
#Earth at 1 AU from Sun
obj2 = GravitationalObject(0.0, 1.495978707*10**11, 30000.0, 0.0, 7000000)
field = GravityField()
field.add_body(obj)
field.add_body(obj2)
print(field)
field.simulate_n_ticks(500)

print(field.history)
