class B(object):
    count = 0
    x = 2

    def __init__(self):
        self.x = 7

    def pr1(self):
        print(self.x)

    @classmethod
    def pr2(cls):
        print(cls.x)
        cls.count += 1


b = B()

print(b.x)#7
print(B.x)#2
b.pr1()#7
#B.pr1()#TypeError
b.pr2()#2
B.pr2()#2