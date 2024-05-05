import numpy  as np
from tau import Tau
import DijkstraAlgorithm as dijkstra
from reading import ReceivedDicts
from Task import Task
from GoldenRatio import GoldenRatioSolver
import copy


def FrankWolf(idsZones, idsLinks, links, tauVal, graphNodesDict, rho, y0, gR, connectDict, epsilon):
    # инициализируем необходимые переменные
    gamma = 0.0
    k = 0
    yk = copy.deepcopy(y0)

    # линеаризируем функцию T
    diff, free = tauVal.LinearValue(yk)

    # применяем алгоритм Дейкстры
    tauValues = tauVal.TauValues(yk)
    zonePath, xp, fk = dijkstra.solve_minT(rho, tauValues, graphNodesDict, idsLinks, links, idsZones, connectDict)

    # строим направление
    pk = fk - yk

    # ищем значение параметра для проверки критерия
    gamma = max(gamma, np.dot(diff, pk) + free)

    while (b := (tauVal.TValue(yk) - gamma) / gamma) > epsilon:
        # находим шаг с помощью метода золотого сечения
        lk = gR.solve(0.00001, yk, pk)
        yk = yk + lk * pk

        # вновь проверяем критерий
        if (tauVal.TValue(yk) - gamma) / gamma < epsilon:
            return yk, k

        # меняем номер итерации
        k += 1

        # вновь линеаризируем функцию T
        diff, free = tauVal.LinearValue(yk)

        # применяем алгоритм Дейкстры
        tauValues = tauVal.TauValues(yk)
        zonePath, xp, fk = dijkstra.solve_minT(rho, tauValues, graphNodesDict, idsLinks, links, idsZones, connectDict)

        # строим направление
        pk = fk - yk

        # ищем значение параметра для проверки критерия
        gamma = max(gamma, np.dot(diff, pk) + free)

    return yk, k, zonePath, xp


def SolveTask():
    # получаем необходимые данные из файлов
    idsZones, idsLinks, links, c, t0, graphNodesDict, rho, connectDict = ReceivedDicts()

    # инициализируем переменные
    tauVal = Tau(t0, c)
    y0 = np.array([0.0] * len(idsLinks))
    t = Task(t0, c)
    gR = GoldenRatioSolver(t)
    epsilon = 0.001

    # находим значения "весов" у ребер или время, которое придется потратить на проезд через каждую дорогу
    tauValues = tauVal.TauValues(y0)

    # применяем алгоритм Дейкстры с этими значениями
    _, _, y0 = dijkstra.solve_minT(rho, tauValues, graphNodesDict, idsLinks, links, idsZones, connectDict)

    # ищем решение задачи с помощью алгоритма Франка-Вульфа
    yk, k, zonePath, xp = FrankWolf(idsZones, idsLinks, links, tauVal, graphNodesDict, rho, y0, gR, connectDict, epsilon)


if __name__ == '__main__':
    SolveTask()


