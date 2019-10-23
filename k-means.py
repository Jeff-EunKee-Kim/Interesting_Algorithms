'''
K-Means Clustering
'''

import math
import numpy as np
import random

# Check if the average converges
def converged(mus, newMus):
    if len(mus) != len(newMus):
        return False
    for i in range(len(mus)):
        if mus[i][0] != newMus[i][0] or mus[i][1] != newMus[i][1] or mus[i][2] != newMus[i][2] or mus[i][3] != newMus[i][3]:
            return False
    return True

# Create clusters
def make_cluster(data, mus):
    clusters = {}

    for d in data:
        closestMu = mus[0]
        minVal = 1000000000000000000
        # any big value 
        for m in mus:
            comp = (d[0]-m[0], d[1]- m[1], d[2]- m[2], d[3]- m[3])
            tempVal = np.linalg.norm(comp)
            if minVal > tempVal:
                minVal = tempVal
                closestMu = m
        try:
            clusters[tuple(closestMu)].append(d)
        except KeyError:
            clusters[tuple(closestMu)] = [d]
    return clusters

# Calculate the new average of the clusters
def calculate_new_center(mus, clusters):
    newMus = []
    for key in clusters.keys():
        newMus.append(np.mean(clusters[key], axis = 0))
    return newMus

# Print results of clusterizing (k-objective, purity)
def print_results(clusters):
    kObjective = 0
    for key in clusters.keys():
        num0 = 0
        num1 = 0
        num2 = 0
        for element in clusters[key]:
            comp = (key[0]-element[0], key[1]- element[1], key[2]- element[2], key[3]- element[3])

            kObjective += (np.linalg.norm(comp))**2

            if element[4] == 0: 
                num0 +=1
            elif element[4] == 1: 
                num1 += 1
            elif element[4] == 2: 
                num2 += 1
        total = num0 + num1 + num2
        mod = 0
        mod = max(num0, num1, num2)
        if mod == num0:
            mod = 0
        elif mod == num1:
            mod = 1
        elif mod == num2:
            mod = 2
        purity = max(num0/total, num1/total, num2/total)
        print("Purity : %f, \\newline Mod : %d" %(purity, mod))  
        print("\\newline")
    print("k-Objective: ", kObjective)
    print("\\newline")
    print("")

# Main k-means algorithm function 
def find_center_of_clusters(data, k, iteration):
    count = 0
    mus = []
    for i in range(k):
        mus.append(data[i])
    newMus = mus
    clusters = {}
    while count == 0 or not converged(mus, newMus):
        count += 1
        mus = newMus
        clusters = make_cluster(data, mus)
        newMus = calculate_new_center(mus, clusters)
        print("Iterations: ", count)
        print("\\newline")
        print_results(clusters)
        if count >= iteration:
            break
    return newMus, clusters

import csv
rows = [] 
  
# reading iris.csv file 
with open("iris.csv") as csvfile: 
    csvreader = csv.reader(csvfile) 
    firstRow = next(csvreader) 
    for row in csvreader: 
        floatRow = [float(a) for a in row]
        rows.append(floatRow) 
  
# Execute the function
find_center_of_clusters(rows, 3, 10)[1]

