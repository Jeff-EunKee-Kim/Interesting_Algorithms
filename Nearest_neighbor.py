'''
Nearest Neighbor Classification

'''

import numpy
import math
import time
import hashlib
import random

def read_data_file(filename):
    file = open(filename)
    data_list = numpy.zeros((1000, 61067))
    for line in file:
        newline = ("".join(line.strip("\n"))).split(",")
        data_point = [int(num) for num in newline]
        data_list[data_point[0] - 1][data_point[1] - 1] = data_point[2]
    return data_list

def get_art_type(filename):
    file = open(filename)
    type_list = []
    for line in file:
        newline = ("".join(line.strip("\n"))).split(",")
        type_list.append(int(newline[0]))
    return type_list

#BRUTE FORCE BELOW 
def brute_force_nn(point_index, data_list, denom_nums):
    max = 0
    max_ind = 7000
    for i in range(len(data_list)):
        if i != point_index:
            val = compute_cos_sim(data_list[point_index], data_list[i], denom_nums[point_index], denom_nums[i])
            if (val > max):
                max = val
                max_ind = i
    return (max_ind)

def compute_cos_sim(point1, point2, mag_x, mag_y):
    numerator = numpy.dot(point1, point2)
    denominator = math.sqrt(mag_x) * math.sqrt(mag_y)
    return float(numerator)/float(denominator)

#LOCALITY SENSITIVE HASHING BELOW
def localSensitiveHash(k, l, data_list):
    #Create the l hash tables
    tables = []
    for i in range(l):
        matrix = numpy.zeros((k,61067))
        for a in range(k):
            for b in range(61067):
                matrix[a][b] = random.uniform(-1,1)
        tables.append(matrix)
    #Create dictionary for buckets for each hash table (2^k in total)
    list_of_dicts = []
    for table in tables:
        dict = {}
        for i in range(1000):
            dummy = []
            point = data_list[i]
            for row in table:
                val = numpy.dot(row,point)
                if val >= 0:
                    dummy.append(1)
                else:
                    dummy.append(-1)
            key = tuple(dummy)
            if key in dict.keys():
                dict[key].append(i)
            else:
                dict[key] = [i]
        list_of_dicts.append(dict)
    return list_of_dicts
    
def testLSH(list_of_dicts, point_index, data_list):
    articles_set = set()
    for dictionary in list_of_dicts:
        for key in dictionary.keys():
            if point_index in dictionary[key]:
                for num in dictionary[key]:
                    articles_set.add(num)
    articles_set.discard(point_index)
    num_of_comps = len(articles_set)
    max = 0
    max_ind = 7000
    for num in articles_set:
        val = compute_cos_sim(data_list[point_index], data_list[num], denom_nums[point_index], denom_nums[num])
        if val > max:
            max = val
            max_ind = num
    return (max_ind, num_of_comps)

## Run Code for testing below (Ctrl + ` to open terminal)
data_list = read_data_file("data.csv")
type_list = get_art_type("label.csv")
denom_nums = [numpy.dot(data_list[i],data_list[i]) for i in range(1000)]

count = 0
for i in range(1000):
    ans = brute_force_nn(i, data_list, denom_nums)
    if type_list[ans] != type_list[i]:
        count += 1
print ("Number of incorrect predictions for brute force algorithm: " + str(count))
print ("Average number of comparisons for brute force algorithm: 999")
print ("---------------------------------------------------------------------------------")
list_of_dicts = localSensitiveHash(4,4,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 4 and l = 4: " + str(count))
print ("Average number of comparisons for k = 4 and l = 4: " + str(avg))
###############################
list_of_dicts = localSensitiveHash(4,8,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 4 and l = 8: " + str(count))
print ("Average number of comparisons for k = 4 and l = 8: " + str(avg))
###############################
list_of_dicts = localSensitiveHash(4,16,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 4 and l = 16: " + str(count))
print ("Average number of comparisons for k = 4 and l = 16: " + str(avg))
###############################
list_of_dicts = localSensitiveHash(8,4,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 8 and l = 4: " + str(count))
print ("Average number of comparisons for k = 8 and l = 4: " + str(avg))
###############################
list_of_dicts = localSensitiveHash(8,8,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 8 and l = 8: " + str(count))
print ("Average number of comparisons for k = 8 and l = 8: " + str(avg))
###############################
list_of_dicts = localSensitiveHash(8,16,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 8 and l = 16: " + str(count))
print ("Average number of comparisons for k = 8 and l = 16: " + str(avg))
###############################
list_of_dicts = localSensitiveHash(16,4,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    #print (ans)
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 16 and l = 4: " + str(count))
print ("Average number of comparisons for k = 16 and l = 4: " + str(avg))
###############################
list_of_dicts = localSensitiveHash(16,8,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 16 and l = 8: " + str(count))
print ("Average number of comparisons for k = 16 and l = 8: " + str(avg))
###############################
list_of_dicts = localSensitiveHash(16,16,data_list)
count = 0
total_num = 0
for i in range(1000):
    (ans,num_of_comps) = testLSH(list_of_dicts, i, data_list)
    total_num += num_of_comps
    if ans == 7000:
        count += 1
    elif type_list[ans] != type_list[i]:
        count += 1
    avg = total_num/1000
print ("Number of incorrect predictions for locality sensitive hashing algorithm when k = 16 and l = 16: " + str(count))
print ("Average number of comparisons for k = 16 and l = 16: " + str(avg))

