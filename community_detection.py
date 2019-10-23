'''
Conductance cut and community detection

'''
import random
import numpy as np
import numpy
import math

# Read files
dep = np.genfromtxt("dep.csv", dtype=int)
A = np.genfromtxt("adj.csv", delimiter=',', dtype=int)

# Find the diagonal matrix
D = np.diag(A.sum(axis=1))

# Find the Laplacian matrix
L = D - A

# Find the eigenvalues and sort it
eigVal, eigVec = np.linalg.eig(L)
sortedEigVal = sorted(eigVal)
# print(eigVal)
# print(eigVec)

# # Find where index of eigVal is 0
# indexWhereEig0 = np.where(eigVal <= 0.01)
# print(indexWhereEig0)
# # Print the 10 smallest eigenvalues
# for i in range(10):
#     print(sortedEigVal[i])

# Random generate 100 researchers


def generateRandom100():
    randList = []
    while len(randList) < 100:
        randList.append(random.randint(0, 1004))
    return randList


def calculateConductance(researcherSet, adjMatrix):
    # Calculate Vol(S) that are within the 100 random generated researchers
    sCount = 0
    for row in researcherSet:
        for col in range(1005):
            if A[row][col] == 1:
                sCount += 1
    # print("Vol(S): ",sCount)

    # Calculate Vol(V-S)
    vmsCount = 0
    for row in range(1005):
        if row in researcherSet:
            continue
        for col in range(1005):
            if A[row][col] == 1:
                vmsCount += 1
    # print("Vol(V-S): ", vmsCount)

    # Calculate cut edges, which would be any edges going out side of the subset
    cutCount = 0
    for row in researcherSet:
        for col in range(1005):
            if col in researcherSet:
                continue
            if A[row][col] == 1:
                cutCount += 1
    # print("Cut edges: ", cutCount)

    # Calculate conductance
    conductance = cutCount / min(sCount, vmsCount)
    # print("Conductance: ", conductance)
    return conductance


conductanceSum = 0
for i in range(5):
    conductanceSum += calculateConductance(generateRandom100(), A)

averageConductance = conductanceSum/5
print("Average Conductance: ", averageConductance)

# 2.c, Finding the conductance of the cut lower than the average
lowCondList = []
for i in range(100):
    lowCondList.append(i)
calculateConductance(lowCondList, A)

indexSort = np.argsort(eigVal)
# print(indexSort)

transposeEigvec = np.transpose(eigVec)

# Transpose the vertex and calculate the distances between each vectors
vertexVector = []
for i in range(1005):
    kVec = []
    for j in range(20):
        currVec = transposeEigvec[indexSort[j+1]]
        kVec.append(currVec[i])
        if len(kVec) == 20:
            break
    vertexVector.append(kVec)

list0 = []
list7 = []
for i in range(len(vertexVector)):
    for0 = np.linalg.norm(
        np.array(vertexVector[0]) - np.array(vertexVector[i]))
    for7 = np.linalg.norm(
        np.array(vertexVector[7]) - np.array(vertexVector[i]))
    list0.append(for0)
    list7.append(for7)

sortedlist0 = np.argsort(list0)
sortedlist7 = np.argsort(list7)

closest0 = []
closest7 = []
minCond0 = 10
minCond7 = 10

for m in range(10, 111):
    print("current group size: ", m)
    community0 = []
    community7 = []
    for i in range(1, m+1):
        community0.append(sortedlist0[i])
        community7.append(sortedlist7[i])

    cond0 = calculateConductance(community0, A)
    cond7 = calculateConductance(community7, A)

    if cond0 < minCond0:
        closest0 = community0
        minCond0 = cond0

    if cond7 < minCond7:
        closest7 = community7
        minCond7 = cond7

print("0: ", closest0)
print("0 length: ", len(closest0))
print("0 community: ", minCond0)
print("7: ", closest7)
print("7 length: ", len(closest7))
print("7 community: ", minCond7)

check0 = [316, 220, 307, 312, 468, 218, 224, 228, 120, 548, 227, 85, 296, 128, 491, 225, 17, 696, 726, 123, 317, 310, 226, 486, 820, 758, 872, 155, 440, 133, 64, 222, 458, 67, 557, 581, 147, 42, 624, 511, 588, 172, 494, 465, 313, 644, 268, 229, 223, 607, 51, 219, 667,
          74, 434, 41, 490, 93, 409, 160, 601, 79, 730, 143, 30, 453, 35, 23, 337, 576, 549, 810, 582, 655, 165, 36, 27, 83, 28, 533, 756, 13, 31, 189, 336, 186, 187, 473, 315, 485, 116, 136, 115, 301, 199, 162, 445, 25, 278, 16, 105, 32, 169, 526, 753, 418, 654, 288, 118, 309]
check7 = [8, 555, 573, 510, 358, 707, 525, 499, 264, 266, 406, 699, 374, 666, 496, 466, 360, 247, 765, 503, 246, 754, 608, 856, 407, 661, 700, 913, 501, 500, 505, 804,
          141, 502, 602, 267, 720, 293, 649, 332, 956, 12, 265, 729, 672, 161, 570, 19, 922, 441, 488, 11, 566, 421, 912, 951, 43, 967, 504, 44, 778, 498, 957, 739, 833, 506]

count0 = 0
count7 = 0
for i in check0:
    if dep[i] == dep[0]:
        count0 += 1
for i in check7:
    if dep[i] == dep[7]:
        count7 += 1

accuracy0 = count0/len(check0)
accuracy7 = count7/len(check7)

print(accuracy0)
print(accuracy7)
