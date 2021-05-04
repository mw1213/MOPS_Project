class GravitationalObject:
    def __init__(self, x0, y0, vx0, vy0, mass):
        self.x = x0
        self.y = y0
        self.vx = vx0
        self.vy = vy0
        self.mass = mass
    
    def __str__ (self):
        return 'GravitationalObject(x=' + str(self.x) + ', y=' + str(self.y) + ', vx=' + str(self.vx) + ', vy=' + str(self.vy) + ', mass=' + str(self.mass) + ')'

Gconst = 6.673*(10**-11)
class GravityField:
    def __init__(self, G=Gconst):
        self.G = G
        self.objects = []

    def __str__(self):
        res = ''
        for i in self.objects:
            res = res + str(i)
            res = res + "\n"
        return res

    def add_body(self, body):
        self.objects.append(body)



print("Gravitational field simulation")
obj = GravitationalObject(10, 20, 30, 40, 50)
obj2 = GravitationalObject(101, 20, 30, 40, 50)
field = GravityField()
field.add_body(obj)
field.add_body(obj2)
print(obj)
print(field)
