from numpy import *
from tau import Tau
import DijkstraAlgorithm as dijkstra
from reading import ReceivedDicts
from Task import Task
from GoldenRatio import GoldenRatioSolver
import copy


def FrankWolf(idsZones, idsLinks, links, tauVal, graphNodesDict, rho, y0, gR, connectDict, epsilon, t):
    gamma = 0.0
    k = 0
    yk = copy.deepcopy(y0)
    #yArr.append(yk)
    diff, free = tauVal.LinearValue(yk)
    tauValues = tauVal.TauValues(yk)

    c = t - tauValues

    zonePath, xp, fk = dijkstra.solve_minT(rho, tauValues, graphNodesDict, idsLinks, links, idsZones, connectDict)
    s = sum(xp)
    pk = fk - yk
    c = dot(diff, pk)
    gamma = max(gamma, dot(diff, pk) + free)
    while (b := (tauVal.TValue(yk) - gamma) / gamma) > epsilon:
        lk = gR.solve(0.00001, yk, pk) # метод золотого сечения
        yk = yk + lk * pk
        if (tauVal.TValue(yk) - gamma) / gamma < epsilon:
            return yk, k
        k += 1

        diff, free = tauVal.LinearValue(yk)
        tauValues = tauVal.TauValues(yk)

        zonePath, xp, fk = dijkstra.solve_minT(rho, tauValues, graphNodesDict, idsLinks, links, idsZones, connectDict)
        pk = fk - yk
        gamma = max(gamma, dot(diff, pk) + free)
    return yk, k, zonePath, xp


def SolveTask():
    # A = array([[1, 1]])  # eq
    idsZones, idsLinks, links, c, t0, graphNodesDict, rho, connectDict = ReceivedDicts()
    tauVal = Tau(t0, c)
    y0 = [len(idsLinks) * 0]
    tauValues = tauVal.TauValues(y0)
    _, _, y0 = dijkstra.solve_minT(rho, tauValues, graphNodesDict, idsLinks, links, idsZones, connectDict)
    t = Task(t0, c)
    gR = GoldenRatioSolver(t)
    epsilon = 0.01

    FrankWolf(idsZones, idsLinks, links, tauVal, graphNodesDict, rho, y0, gR, connectDict, epsilon, tauValues)


if __name__ == '__main__':
    SolveTask()


