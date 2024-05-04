from functions import integrValue, funcValue
import numpy as np


class Tau:
    def __init__(self, t0, c) -> None:
        self.t0 = t0
        self.c = c

    def LinearValue(self, point):
        free = self.TValue(point)
        diff = self.TauValues(point)
        return diff, free

    def TauValues(self, point):
        return funcValue(point, self.t0, self.c)

    def TValue(self, point):
        return sum(integrValue(point, self.t0, self.c))
