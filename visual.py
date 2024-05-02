import networkx as nx
import matplotlib.pyplot as plt
import geopandas as gpd
import pandas as pd
from shapely.geometry import Point
import numpy as np


def ReadFirstLine(f):
    string = f.readline()
    while string[0] != "$":
        string = f.readline()
    string = f.readline()
    return string


def ReadNodes(fileName):
    directName = "input_data"
    ids = []
    # x = []
    # y = []
    coordinates = []
    f = open(directName + fileName, "r")
    string = ReadFirstLine(f)
    while string != "":
        numbers = string.split(";")
        ids.append(int(numbers[0]))
        coordinates.append([float(numbers[1]), float(numbers[2][:-1])])
        # x.append(numbers[1])
        # y.append(numbers[2])
        string = f.readline()
    f.close()
    coordinates = np.asarray(coordinates)
    return ids, coordinates


def ReadConnectors(fileName):
    directName = "input_data"
    x = []
    y = []
    f = open(directName + fileName, "r")
    string = ReadFirstLine(f)
    while string != "":
        numbers = string.split(";")
        x.append(int(numbers[0]))
        y.append(int(numbers[1]))
        string = f.readline()
    f.close()
    return x, y


def ReadLinks(fileName):
    directName = "input_data"
    ids = []
    x = []
    y = []
    f = open(directName + fileName, "r")
    string = ReadFirstLine(f)
    while string != "":
        numbers = string.split(";")
        if int(numbers[4]) != 0:
            ids.append(int(numbers[0]))
            x.append(int(numbers[1]))
            y.append(int(numbers[2]))
        string = f.readline()
    f.close()
    return ids, x, y


def Draw(ids, x, y, linksIds, fromNode, toNode):
    G = nx.DiGraph(directed=True)
    pos = {}
    for i, id in enumerate(ids):
        G.add_node(id)
        pos[id] = (x[i], y[i])
    nx.set_node_attributes(G, pos, "coord")
    for i, id in enumerate(fromNode):
        G.add_edge(id, toNode[i])
    nx.draw(G, pos, node_size = 10)
    plt.show()


def ConvertDegToRad(degree):
    return degree * (np.pi / 180.0)


def ConvertToCartesian(polar):
    polar[:, 1] = ConvertDegToRad(polar[:, 1])
    a = np.reshape(polar[:, 0] * np.cos(polar[:, 1]), (-1, 1))
    b = np.reshape(polar[:, 0] * np.sin(polar[:, 1]), (-1, 1))

    cartesian = np.hstack([a, b])
    return cartesian


if __name__ == '__main__':
    ids, coordinates = ReadNodes("\input_nodes.net")
    coordinates = ConvertToCartesian(coordinates)
    dictionary = dict(zip(ids, coordinates))
    df = pd.DataFrame(coordinates)
    df['coordinates'] = df[[0, 1]].values.tolist()
    df['coordinates'] = df['coordinates'].apply(Point)
    df = gpd.GeoDataFrame(df, geometry='coordinates')
    ax_all=df.plot(markersize=3, marker='o')

    ids, coordinates = ReadNodes("\input_zones.net")
    coordinates = ConvertToCartesian(coordinates)
    dictionaryZones = dict(zip(ids, coordinates))
    df2 = pd.DataFrame(coordinates)
    df2['coordinates'] = df2[[0, 1]].values.tolist()
    df2['coordinates'] = df2['coordinates'].apply(Point)
    df2 = gpd.GeoDataFrame(df2, geometry='coordinates')
    df2.plot(ax=ax_all, markersize=30, facecolors='none', edgecolors='r')

    ids, fromNode, toNode = ReadLinks("\input_links.net")
    for i, _ in enumerate(ids):
        fCoord = dictionary[fromNode[i]]
        sCoord = dictionary[toNode[i]]
        plt.plot([fCoord[0], sCoord[0]], [fCoord[1], sCoord[1]], linewidth=0.1, linestyle="-", color="k")

    fromZone, toNode = ReadConnectors("\input_connectors.net")
    for i, _ in enumerate(fromZone):
        fCoord = dictionaryZones[fromZone[i]]
        sCoord = dictionary[toNode[i]]
        plt.plot([fCoord[0], sCoord[0]], [fCoord[1], sCoord[1]], linewidth=0.5, linestyle="-", color="r")

    plt.show()
