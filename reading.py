import numpy as np


directName = "input_data"


def ReadFirstLine(f):
    string = f.readline()
    while string[0] != "$":
        string = f.readline()
    string = f.readline()
    return string


def ReadNodes(fileName):
    ids = []
    f = open(directName + fileName, "r")
    string = ReadFirstLine(f)
    while string != "":
        numbers = string.split(";")
        ids.append(int(numbers[0]))
        # x.append(numbers[1])
        # y.append(numbers[2])
        string = f.readline()
    f.close()
    return ids


def ReadConnectors(fileName):
    x = []
    y = []
    f = open(directName + fileName, "r")
    string = ReadFirstLine(f)
    while string != "":
        numbers = string.split(";")
        if numbers[2] == "D":
            x.append(int(numbers[0]))
            y.append(int(numbers[1]))
        else:
            x.append(int(numbers[1]))
            y.append(int(numbers[0]))
        string = f.readline()
    f.close()
    return x, y


def ReadLinks(fileName):
    ids = []
    x = []
    y = []
    t = []
    c = []
    f = open(directName + fileName, "r")
    string = ReadFirstLine(f)
    while string != "":
        numbers = string.split(";")
        if int(numbers[4]) != 0:
            ids.append(int(numbers[0]))
            x.append(int(numbers[1]))
            y.append(int(numbers[2]))
            c.append(float(numbers[5])/1440.0)
            t.append(float(numbers[3])/float(numbers[6]))
        string = f.readline()
    f.close()
    c = np.array(c)
    t = np.array(t)
    ids = np.array(ids)
    return ids, x, y, c, t


def ReadSOD(fileName):
    x = []
    y = []
    values = []
    f = open(directName + fileName, "r")
    ReadFirstLine(f)
    string = ReadFirstLine(f)
    while string != "":
        numbers = string.split(";")
        if float(numbers[2]) != 0.0:
            x.append(int(numbers[0]))
            y.append(int(numbers[1]))
            values.append(float(numbers[2]))
        string = f.readline()
    f.close()
    return x, y, values


def ReceivedDicts():
    idsNodes = ReadNodes("\input_nodes.net")

    idsZones = ReadNodes("\input_zones.net")

    idsLinks, fromNode, toNode, c, t = ReadLinks("\input_links.net")
    # linksDict = dict(zip(idsLinks, [[i, toNode[id]] for id, i in enumerate(fromNode)]))
    links = [[i, toNode[id]] for id, i in enumerate(fromNode)]

    idsNodes = idsZones + idsNodes

    graphNodesDict = dict(zip(idsNodes, [[] for _ in range(len(idsNodes))]))
    for id, node in enumerate(fromNode):
        graphNodesDict[node].append(toNode[id])

    fromZone, toNode = ReadConnectors("\input_connectors.net")
    for id, node in enumerate(fromZone):
        graphNodesDict[node].append(toNode[id])
    connectDict = dict(zip(idsZones, [[] for _ in range(len(idsZones))]))
    for id, node in enumerate(toNode):
        if node in idsZones:
            connectDict[node].append(fromZone[id])

    fromZone, toZone, values = ReadSOD("\input_sod.net")
    SOD = np.zeros((len(idsZones), len(idsZones)))
    for id, zone in enumerate(fromZone):
        i = idsNodes.index(zone)
        j = idsNodes.index(toZone[id])
        SOD[i, j] = values[id]

    return idsZones, idsLinks, links, c, t, graphNodesDict, SOD, connectDict

