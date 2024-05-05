# import sys
#
#
# class Graph(object):
#     def __init__(self, nodes, init_graph):
#         self.nodes = nodes
#         self.graph = self.construct_graph(nodes, init_graph)
#
#     def construct_graph(self, nodes, init_graph):
#         '''
#         Этот метод обеспечивает симметричность графика: если существует путь от узла A к B со значением V, должен быть путь от узла B к узлу A со значением V.
#         '''
#         graph = {}
#         for node in nodes:
#             graph[node] = {}
#
#         graph.update(init_graph)
#
#         for node, edges in graph.items():
#             for adjacent_node, value in edges.items():
#                 if graph[adjacent_node].get(node, False) == False:
#                     graph[adjacent_node][node] = value
#
#         return graph
#
#     def get_nodes(self):
#         "Возвращает узлы графа"
#         return self.nodes
#
#     def get_outgoing_edges(self, node):
#         "Возвращает соседей узла"
#         connections = []
#         for out_node in self.nodes:
#             if self.graph[node].get(out_node, False) != False:
#                 connections.append(out_node)
#         return connections
#
#     def value(self, node1, node2):
#         "Возвращает значение ребра между двумя узлами."
#         return self.graph[node1][node2]
#
#
# def dijkstra_algorithm(graph, start, toZones, tauValues, links, idsLinks, idsZones):
#     visitedNodes = list(len(graph.))
#     shortest_path = {}
#     previous_nodes = {}
#     # Мы будем использовать max_value для инициализации значения "бесконечности" непосещенных узлов
#     max_value = sys.maxsize
#     for node in unvisited_nodes:
#         shortest_path[node] = max_value
#     # Однако мы инициализируем значение начального узла 0
#     shortest_path[start_node] = 0
#     while unvisited_nodes:
#         current_min_node = None
#         for node in unvisited_nodes:  # Iterate over the nodes
#             if current_min_node == None:
#                 current_min_node = node
#             elif shortest_path[node] < shortest_path[current_min_node]:
#                 current_min_node = node
#                 neighbors = graph.get_outgoing_edges(current_min_node)
#                 for neighbor in neighbors:
#                     tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
#                     if tentative_value < shortest_path[neighbor]:
#                         shortest_path[neighbor] = tentative_value
#                         # Мы также обновляем лучший путь к текущему узлу
#                         previous_nodes[neighbor] = current_min_node
#                         unvisited_nodes.remove(current_min_node)
#     return previous_nodes, shortest_path

import numpy as np
import copy
import heapq


def dijkstra(graph, start, tauValues, links, idsLinks, idsZones):
    # поиск подходящей вершины
    visited = {vertex: False for vertex in graph}
    for i in idsZones:
        visited[i] = True
    dist = {vertex: np.inf for vertex in graph}
    path = {vertex: [] for vertex in graph}
    pq = []
    dist[start] = 0
    for i in graph[start]:
        dist[i] = 0
        heapq.heappush(pq, (0, i))

    while pq:
        currentDist, currentVertex = heapq.heappop(pq)
        while visited[currentVertex] == True:
            if len(pq) == 0:
                return path, dist
            currentDist, currentVertex = heapq.heappop(pq)

        visited[currentVertex] = True
        for neighbor in graph[currentVertex]:
            if visited[neighbor] == True:
                continue
            index = links.index([currentVertex, neighbor])
            distance = currentDist + tauValues[index]
            if distance < dist[neighbor]:
                dist[neighbor] = distance
                path[neighbor].clear()
                path[neighbor] = copy.deepcopy(path[currentVertex])
                path[neighbor].append(index)
                heapq.heappush(pq, (distance, neighbor))
            # elif distance == dist[neighbor]:
            #     way1 = copy.deepcopy(path[currentVertex])
            #     way1.append(idsLinks[index])
            #
            #     if len(path[neighbor]) > 0 and isinstance(path[neighbor][0], list):
            #         ways = []
            #         for list1 in path[neighbor]:
            #             ways.append(copy.deepcopy(list1))
            #         path[neighbor].clear()
            #         path[neighbor].extend(ways)
            #     else:
            #         ways = copy.deepcopy(path[neighbor])
            #         path[neighbor].clear()
            #         path[neighbor].append(ways)
            #     path[neighbor].append(way1)

        # distSorted = list(dist.values())
        # distSorted.sort()
        # found = False
        # while len(distSorted) > 0 and found == False:
        #     minDist = distSorted[0]
        #     suitVerts = [key for key, value in dist.items() if value == minDist]
        #     for vert in suitVerts:
        #         if visited[vert] == False:
        #             currentVertex = vert
        #             found = True
        #             break
        #     while found == False and len(distSorted) > 0 and distSorted[0] == minDist:
                # distSorted.pop(0)
        # if distSorted[0] == np.inf:
        #     return path, dist

    return path, dist


def solve_minT(rho, tauValues, graphNodesDict, idsLinks, links, idsZones, connectDict):
    graph = graphNodesDict
    ye = np.array([0.0] * len(idsLinks))
    zonePath = []
    xp = []
    for id, fromZone in enumerate(idsZones):
        toZones = [n for n, i in enumerate(rho[id]) if i > 0]
        if len(toZones) > 0:
            # toNodes = []
            # for k in toZones:
            #     toNodes.append(graph[idsZones[k]])
            path, dist = dijkstra(graph, fromZone, tauValues, links, idsLinks, idsZones)
            for toZone in toZones:
                toNodes = connectDict[idsZones[toZone]]
                minDist = np.inf
                minNode = 0
                for node in toNodes:
                    if dist[node] < minDist:
                        minDist = dist[node]
                        minNode = node
                way = path[minNode]
                temp = copy.deepcopy(way)
                temp.append(toZone)
                zonePath.append([id] + temp)
                # if isinstance(way[0], list):
                #     for w in way:
                #         for e in w:
                #             index = np.where(idsLinks == e)
                #             ye[index[0]] += rho[id][zone] / len(way)
                # else:
                for e in way:
                    ye[e] += rho[id][toZone]
                xp.append(rho[id][toZone])

    return zonePath, xp, ye


# Define problem parameters
# y_k = np.array([1, 2, 3])
# grad_T = np.array([1, 1, 1])
# A = np.array([[1, -1, 1], [1, 1, 1]])
# b = np.array([3, 5])
#
# # Solve the optimization problem
# minT_solution = solve_minT(y_k, grad_T, A, b)
# print(minT_solution)