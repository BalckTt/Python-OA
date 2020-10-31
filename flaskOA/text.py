class A:
    e = "动物"
    def x(self,d):
        print(f"属于{A.e}",end="")
        print(f"我能{d.e}")

class B:
    e="能飞的"
    def __init__(self):
        print("我是麻雀",end="")

class C:
    e="肉食动物"
    def __init__(self):
        print("我是狮子",end="")

a = A()
b = B()
a.x(b)
c = C()
a.x(c)
