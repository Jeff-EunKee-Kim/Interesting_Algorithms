'''
Huffman Coding

'''

# * <--------------------------------   Importing libraries -------------------------------------------->

import heapq
import numpy as np
import hashlib
import random

# * <--------------------------------   Huffman Coding -------------------------------------------->


class HuffNode:
    def __init__(self, char, freq, left, right):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        if (other == None):
            return False
        if (not isinstance(other, HuffNode)):
            return False
        return self.freq == other.freq


class HuffmanEncoding:
    def __init__(self):
        self.heap = []
        self.char_to_bits = {}
        self.bits_to_char = {}

    def BuildHuffmanCodeTree(self, chars, freqs):
        #Step 1: Make dictionary of characters/frequencies
        dict = self.make_freq_dict(chars, freqs)
        #Step 2: make priority queue heap
        self.make_heap(dict)
        #Step 3: build huffman tree
        huffHead = self.make_tree()
        #Step 4: Put encodings in the dictionaries
        self.write_encodings(huffHead, "")

    def make_freq_dict(self, char_list, freq_list):
        freq_dict = {}
        for i in range(len(char_list)):
            freq_dict[char_list[i]] = int(freq_list[i])
        return freq_dict

    def make_heap(self, dict):
        for char in dict.keys():
            node = HuffNode(char, dict[char], None, None)
            heapq.heappush(self.heap, node)

    def make_tree(self):
        while (len(self.heap) > 1):
            left = heapq.heappop(self.heap)
            right = heapq.heappop(self.heap)
            new_node = HuffNode(-1, left.freq + right.freq, left, right)
            heapq.heappush(self.heap, new_node)
        head = heapq.heappop(self.heap)
        return head

    def write_encodings(self, huffTree, string):
        if (huffTree == None):
            return
        elif (huffTree.left == None and huffTree.right == None):
            self.char_to_bits[huffTree.char] = string
            self.bits_to_char[string] = huffTree.char
        else:
            self.write_encodings(huffTree.left, string+"0")
            self.write_encodings(huffTree.right, string+"1")

    def Encode(self, string):
        bit_string = ""
        for char in string:
            bit_string = bit_string + str(self.char_to_bits[char])
        print("Length of encoded message is " + str(len(bit_string)))
        return bit_string

    def Decode(self, string):
        decoded_string = ""
        encoded_string = ""
        for bit in string:
            encoded_string += bit
            if encoded_string in self.bits_to_char.keys():
                decoded_string += self.bits_to_char[encoded_string]
                encoded_string = ""
        return decoded_string


# Alphabet/Frequency/Message 1
file = open("Alphabet1.txt")
alph1 = file.readline()
alph1_list = []
i = 0
while (i < len(alph1)):
    alph1_list.append(alph1[i])
    i = i + 2

file = open("Frequency1.txt", "r")
freq1 = file.readline()
freq1_list = ("".join(freq1)).split(",")
freq1_list.remove("")

huff = HuffmanEncoding()
huff.BuildHuffmanCodeTree(alph1_list, freq1_list)
file = open("Message1.txt")
msg1 = file.readline()
print("Message 1")
print("Size of original message is " + str(len(msg1)))
print("Size of alphabet is " + str(len(alph1_list)))
encoded_msg1 = huff.Encode(msg1)
print("----------------------------------------------")

# Alphabet/Frequency/Message 2
file = open("Alphabet2.txt", "r")
alph2 = file.readline()
alph2_list = []
i = 0
while (i < len(alph2)):
    alph2_list.append(alph2[i])
    i = i + 2

file = open("Frequency2.txt", "r")
freq2 = file.readline()
freq2_list = ("".join(freq2)).split(",")
freq2_list.remove("")

huff = HuffmanEncoding()
huff.BuildHuffmanCodeTree(alph2_list, freq2_list)
file = open("Message2.txt")
msg2 = file.readline()
print("Message 2")
print("Size of original message is " + str(len(msg2)))
print("Size of alphabet is " + str(len(alph2_list)))
encoded_msg2 = huff.Encode(msg2)
