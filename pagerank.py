'''
Pagerank

''' 

import random
import numpy as np
import numpy
import math


def readfile(filename):
    file = open(filename)
    adj_matrix = []
    for line in file:
        newline = ("".join(line.strip("\n"))).split(",")
        adj_entry = [int(num) for num in newline]
        adj_matrix.append(adj_entry)
    return adj_matrix


def indegree_rank(matrix):
    list = [(i+1, 0) for i in range(1000)]
    articles = []
    print(len(matrix))
    for i in range(len(matrix)):
        entry = matrix[i]
        for j in range(len(entry)):
            if entry[j] == 1:
                list[j] = (list[j][0], list[j][1] + 1)
    list.sort(key=lambda tup: tup[1])
    size = len(matrix) - 1
    for i in range(10):
        articles.append(list[size-i])
    return articles


def pagerank(adj_matrix, trans_matrix, tolerance):
    startProb = 1/float(len(adj_matrix))
    num_of_iter = 0
    state = numpy.asarray([startProb for i in range(len(adj_matrix))])
    while True:
        oldState = state
        state = numpy.dot(state, trans_matrix)
        num_of_iter += 1
        TVD = 0
        #Calulating the TVD(x,y) value
        for i in range(len(oldState)):
            TVD += abs(state[i] - oldState[i])
        TVD = .5*TVD
        if TVD < tolerance:
            break
        #Answering question 2
        if num_of_iter == 1:
            sorted_state = numpy.sort(state)[::-1]
            arr = []
            for i in range(10):
                result = numpy.where(state == sorted_state[i])
                arr.append((result, sorted_state[i]))
            print("Top 10 articles after one iteration:")
            print(arr)
    sorted_state = numpy.sort(state)[::-1]
    arr = []
    for i in range(10):
        result = numpy.where(state == sorted_state[i])
        arr.append((result, sorted_state[i]))
    print("Top 10 articles after final iteration:")
    print(arr)
    print("Total number of iterations is " + str(num_of_iter))
    return


def create_transitionMatrix(adj_matrix):
    n = len(adj_matrix)
    trans_matrix = [[0 for i in range(len(adj_matrix))]
                    for i in range(len(adj_matrix))]
    for i in range(len(trans_matrix)):
        d_i = sum(adj_matrix[i])
        for j in range(len(trans_matrix)):
            if d_i == 0:
                trans_matrix[i][j] = 1/float(n)
            else:
                trans_matrix[i][j] = .15/float(n) + (.85*adj_matrix[i][j])/d_i
    return trans_matrix


adj_matrix = readfile("citations.csv")
#adj_matrix = [[0,1,1,0], [0,0,0,1], [1,1,0,1], [0,0,1,0]]
adj_matrix = numpy.asarray(adj_matrix)
q3 = indegree_rank(adj_matrix)
print("The 10 articles with the highest indegree rankings are: " + str(q3))
trans_matrix = create_transitionMatrix(adj_matrix)
trans_matrix = numpy.asarray(trans_matrix)
pagerank(adj_matrix, trans_matrix, .001)