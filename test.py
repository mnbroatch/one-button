a = lambda self: self.x

class A:
    b = a
    x = 4

p = A()

print(p.b())
