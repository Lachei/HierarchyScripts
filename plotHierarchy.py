from struct import pack, unpack
import os
import numpy as np
import matplotlib.pyplot as plt
import math
import hierarchyImporter as hi

baseFolder = "/run/media/lachei/3d02119e-bc93-4969-9fc5-523f06321708/hierarchy"
baseAlpha = .00001

if False:
    x, y, counts = hi.openAttributeCenters(baseFolder)
    alphas = [1 - math.pow(1 - baseAlpha, count) for count in counts]
    plt.scatter(x, y, alpha = alphas)
    plt.show()

axisValues = hi.openAttributeAxisValues(baseFolder)
print(len(axisValues[0]))
combinations, clusterCenter, clusterCounts = hi.openClusters(baseFolder)

x1, y1, x2, y2, alphas = [], [], [], [], []
for c in range(len(combinations)):
    combination = combinations[c]
    if combination[1] - combination[0] > 1:
        continue
    print("successive parameters", combination)
    amtOfCluster = len(clusterCounts[c])
    axisA, axisB = int(combination[0]), int(combination[1])
    x1 += [axisA] * amtOfCluster
    x2 += [axisB] * amtOfCluster
    y1 += [ind[0]/1000.0 for ind in clusterCenter[c]]
    y2 += [ind[1]/1000.0 for ind in clusterCenter[c]]
    alphas += [1 - math.pow(1-baseAlpha, count) for count in clusterCounts[c]]

testpoints = []
for i in range(10):
    testpoints.append([])
    testpoints[-1].append(x1[i])
    testpoints[-1].append(y1[i])
    testpoints[-1].append(x2[i])
    testpoints[-1].append(y2[i])
print(testpoints)

print(len(x1), len(x2), len(y1), len(y2))

amt = len(x1)
for i in range(amt):
    plt.plot([x1[i], x2[i]], [y1[i], y2[i]], 'b', alpha = alphas[i])

plt.show()
