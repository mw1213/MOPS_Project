import copy

Gconst = 6.673*(10**-11)

class GravitationalObject:
    def __init__(self, x0, y0, vx0, vy0, mass):
        self.x = x0
        self.y = y0
        self.vx = vx0
        self.vy = vy0
        self.mass = mass
        self.acc_x = 0
        self.acc_y = 0.0
    
    def __str__ (self):
        return 'GravitationalObject(x=' + str(self.x) + ', y=' + str(self.y) + ', vx=' + str(self.vx) + ', vy=' + str(self.vy) + ', mass=' + str(self.mass) + ')'
    
    def __repr__(self):
        return str(self)

    def acceleration_from_other_object(self, other):
        force_x = Gconst*self.mass*other.mass/(abs(self.x-other.x))**2
        force_y = Gconst*self.mass*other.mass/(abs(self.y-other.y))**2
        acc_x = force_x/self.mass
        acc_y = force_y/self.mass
        return [acc_x, acc_y]


    def move_a_tick(self, accelerations, tick=1):
        self.x = self.x + self.vx * tick + accelerations[0] * tick**2 / 2
        self.y = self.y + self.vy * tick + accelerations[1] * tick**2 / 2

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
                    acc[0] = acc[0] - i.acceleration_from_other_object(j)[0]
                    acc[1] = acc[1] - i.acceleration_from_other_object(j)[1]                    
            objects_acc.append(acc)

        #calculate new positions of objects: tick means t = 1
        t = 1
        for x, obj in enumerate(self.objects):
            obj.move_a_tick(objects_acc[x], t)







print("Gravitational field simulation")
obj = GravitationalObject(10.0, 20.0, 30.0, 40.0, 50.0)
obj2 = GravitationalObject(101.0, 40.0, 30.0, 40.0, 70.0)
obj3 = GravitationalObject(21.0, -60.0, 30.0, 40.0, 110.0)
field = GravityField()
field.add_body(obj)
field.add_body(obj2)
print(field)
field.tick()
field.tick()

print(field.history)