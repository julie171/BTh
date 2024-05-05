import numpy as np
import copy
import heapq


def dijkstra(graph, start, tauValues, links, idsZones):
    # словарь для посещённых вершин
    visited = {vertex: False for vertex in graph}

    # все зоны посещены, чтобы в них не заходить
    for i in idsZones:
        visited[i] = True

    # инициализация
    dist = {vertex: np.inf for vertex in graph}
    path = {vertex: [] for vertex in graph}
    pq = []
    dist[start] = 0

    # расстояния до всех вершин, соединенных коннекторами в начальной зоной, равны 0
    for i in graph[start]:
        dist[i] = 0
        heapq.heappush(pq, (0, i))

    while pq:
        # ищем вершину с наименьшим расстоянием и которую еще не посещали
        currentDist, currentVertex = heapq.heappop(pq)
        while visited[currentVertex] == True:
            if len(pq) == 0:
                return path, dist
            currentDist, currentVertex = heapq.heappop(pq)

        # отмечаем, что вершина посещена
        visited[currentVertex] = True

        # рассматриваем расстояния до соседей данной вершины
        for neighbor in graph[currentVertex]:
            # пропускаем вершины, которые уже посетили
            if visited[neighbor] == True:
                continue

            # считаем расстояние до соседней вершины через данную
            index = links.index([currentVertex, neighbor])
            distance = currentDist + tauValues[index]

            # если нашли меньшее расстояние, меняем путь и расстояние до вершины и записываем ее в вершины, которые нужно посетить
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                path[neighbor].clear()
                path[neighbor] = copy.deepcopy(path[currentVertex])
                path[neighbor].append(index)
                heapq.heappush(pq, (distance, neighbor))

    return path, dist


def solve_minT(rho, tauValues, graphNodesDict, idsLinks, links, idsZones, connectDict):
    # инициализация переменных
    graph = graphNodesDict
    ye = np.array([0.0] * len(idsLinks))
    zonePath = []
    xp = []

    for id, fromZone in enumerate(idsZones):
        # поиск зон, к которым кто-то хочет проехать из данной зоны
        toZones = [n for n, i in enumerate(rho[id]) if i > 0]

        if len(toZones) > 0:
            # применяем алгоритм Дейкстры для данной подходящей зоны
            path, dist = dijkstra(graph, fromZone, tauValues, links, idsZones)

            # расписываем оптимальные пути из данной зоны в те, к которым кто-то хочет проехать, через вершины, соединенные коннекторами
            for toZone in toZones:
                toNodes = connectDict[idsZones[toZone]]
                minDist = np.inf
                minNode = 0
                for node in toNodes:
                    if dist[node] < minDist:
                        minDist = dist[node]
                        minNode = node
                way = path[minNode]

                # записываем путь с началом и концом в виде зон, которые этот путь соединяет
                temp = copy.deepcopy(way)
                temp.append(toZone)
                zonePath.append([id] + temp)

                # расписываем загруженность дорог, используя ограничения
                for e in way:
                    ye[e] += rho[id][toZone]

                # поток по пути
                xp.append(rho[id][toZone])

    return zonePath, xp, ye
