from functions import integrValue


class Task:
    def __init__(self, t0, c):
        self.a = 0
        self.b = 1
        self.t0 = t0
        self.c = c

    def func(self, point):
        return sum(integrValue(point, self.t0, self.c))