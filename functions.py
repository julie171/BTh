import numpy as np


def integrValue(v: np.array, t0: np.array, c: np.array) -> np.array:
    funcsValues = v * t0 * (1 + np.power(np.divide(v, c), 4) * 0.03)
    return funcsValues


def funcValue(v: np.array, t0: np.array, c: np.array) -> np.array:
    diffValues = t0 * (1 + 0.15 * np.power(np.divide(v, c), 4))
    return diffValues
