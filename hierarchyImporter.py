from struct import pack, unpack
import os
import numpy as np
import matplotlib.pyplot as plt
import math

# opens the attributeCenters.ac file and extracts infos
# baseFolder    : Path of the base folder containing the attributeCenters.ac and attr.info files
# return        : A tuple of (x, y, counts) with the x-coordinates (x), the y-coordinates(y) and the amt of datapoints falling into the respective x,y point (counts)
# example usage : x, y, counts = openAttributeCenters(myHierarchyFolder)
def openAttributeCenters(baseFolder):
    lvlAmt = 3
    class Object(object):
        pass

    acFile = baseFolder + "/attributeCenters.ac"
    attributeInfo = baseFolder + "/attr.info"
    byteSize = os.path.getsize(acFile)
    with open(acFile) as file, open(attributeInfo) as aInfo:
        attributes = []
        firstLine = True
        for line in aInfo:
            if firstLine:
                firstLine = False
                continue
            words = line.split()
            a = Object()
            a.name = words[0]
            a.min = words[1]
            a.max = words[2]
            attributes.append(a)

        binaryData = np.fromfile(acFile, dtype=np.uint32)

        lvls = []
        lvls.append([])
        lvls.append([])
        lvls.append([])
        curInd = 0
        for i in range(len(attributes)):
            for l in range(lvlAmt):
                lvls[l].append((binaryData[curInd], binaryData[curInd + 1],))
                curInd += 2

        # making a plot for lvl 3 with points
        x = []  # holding the attribute locations [0, len(attributes))
        y = []  # holding the center values [0, 1]
        counts = [] # holding the counts for the center values
        for a in range(len(lvls[2])):
            amtOfCenters = int(lvls[2][a][1] / 4 / 4)
            offset = int(lvls[2][a][0] / 4)
            for c in range(amtOfCenters):
                x.append(a)
                raw = binaryData[offset + 4 * c]
                count = binaryData[offset + 4 * c + 3]
                center = unpack('f', pack('I', raw))
                y.append(center)
                counts.append(count)

        return (x, y, counts,)

# opens the attributeCenters.ac file and extracts infos
# baseFolder    : Path of the base folder containing the attributeCenters.ac and attr.info files
# return        : A tuple of (x, y, counts) with the x-coordinates (x), the y-coordinates(y) and the amt of datapoints falling into the respective x,y point (counts)
# example usage : x, y, counts = openAttributeCenters(myHierarchyFolder)
def openAttributeAxisValues(baseFolder):
    lvlAmt = 3
    class Object(object):
        pass

    acFile = baseFolder + "/attributeCenters.ac"
    attributeInfo = baseFolder + "/attr.info"
    byteSize = os.path.getsize(acFile)
    with open(acFile) as file, open(attributeInfo) as aInfo:
        attributes = []
        firstLine = True
        for line in aInfo:
            if firstLine:
                firstLine = False
                continue
            words = line.split()
            a = Object()
            a.name = words[0]
            a.min = words[1]
            a.max = words[2]
            attributes.append(a)

        binaryData = np.fromfile(acFile, dtype=np.uint32)

        lvls = []
        lvls.append([])
        lvls.append([])
        lvls.append([])
        curInd = 0
        for i in range(len(attributes)):
            for l in range(lvlAmt):
                lvls[l].append((binaryData[curInd], binaryData[curInd + 1],))
                curInd += 2

        # extracting all axis values for each axis
        axisVals = []
        for a in range(len(lvls[2])):
            axisVals.append([])
            amtOfCenters = int(lvls[2][a][1] / 4 / 4)
            offset = int(lvls[2][a][0] / 4)
            for c in range(amtOfCenters):
                raw = binaryData[offset + 4 * c]
                center = unpack('f', pack('I', raw))
                axisVals[-1].append(center)

        return axisVals

# opens the cluster data file and parses its contents
# baseFolder    : The hierarchy base folder containing the combination.info and cluster.cd file
# return        : A tuple (combinations, clusterCenter, clusterCounts), where combinations is a 2d list containing attribute indices for each attribute combination,
#                   clusterCenter is a list of 2d list where each 2d list corresponds to a single combination of attributes from combinations and stores per row the cneter indices corresponding to the current cluster,
#                   and clusterCounts is a 2d list, where for each row corresponds to a single combination of attributes form combinations and each element of the row corresponds to one row of the clusterCenter describing the amount of datapoints going through that cluster
def openClusters(baseFolder):
    class Object(object):
        pass
    combinationFile = baseFolder + "/combination.info"
    clusterDataFile = baseFolder + "/cluster.cd"

    byteSize = os.path.getsize(clusterDataFile)
    with open(combinationFile) as combinationF, open(clusterDataFile) as clusterDataF:
        #reading the combination information
        combinations = []
        for line in combinationF:
            combInds = line.split()
            combinations.append([int(x) for x in combInds])

        #reading the data
        binaryData = np.fromfile(clusterDataF, dtype = np.uint32)

        clusterOffsetRanges = []
        curInd = 0
        for i in range(len(combinations)):
            clusterOffsetRanges.append([])
            clusterOffsetRanges[-1].append(binaryData[curInd])
            clusterOffsetRanges[-1].append(binaryData[curInd + 1])
            curInd += 2
        alignedIndexSize = (len(combinations[0]) + 1) >> 1

        clusters = []
        clusterCounts = []

        packingString = 'I' * (alignedIndexSize + 1)
        unpackingString = 'H' * (2 * alignedIndexSize) + 'I'
        print('packing with', packingString)
        print('unpacking with', unpackingString)

        for i in range(len(combinations)):
            clusters.append([])
            clusterCounts.append([])
            amtOfCluster = int(clusterOffsetRanges[i][1] / (alignedIndexSize + 1) / 4)
            for c in range(amtOfCluster):
                startInd = int(clusterOffsetRanges[i][0] / 4 + (alignedIndexSize + 1) * c)
                clusterInfo = binaryData[startInd: startInd + alignedIndexSize + 1]
                try:
                    infos = unpack(unpackingString, pack(packingString, *clusterInfo))
                except:
                    print(startInd, startInd + alignedIndexSize + 1, clusterInfo)
                    return
                clusters[-1].append(infos[0:len(combinations[0])])
                clusterCounts[-1].append(infos[-1])

        return (combinations, clusters, clusterCounts)

