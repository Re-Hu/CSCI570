"""
CSCI570 final Project - ReadandWrite.py
Author: Xiaoyue Hu
Read input file, extend the string, and write output file
"""

import sys
from resource import *
import time
import psutil

# inputfile = sys.argv[1]
# outfile = sys.argv[2]
inputfile = "input4.txt"
outfile_b = "outputbasic.txt"
outfile_e = "outputefficient.txt"
def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper():
    start_time = time.time()
    call_algorithm()
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    return time_taken

def ReadInput(inputfile):
    with open(inputfile, 'r') as f:
        lines = f.readlines()
        # word = {}
        word = []
        word_index = -1
        index = []
        string = ""
        for i in lines:
            line = i.strip()
            if not line.isdigit():
                # word[line.strip()] = []
                word.append(line.strip())
                word_index += 1
                index.append([])
                # string = line.strip()
            else:
                # word[string].append(int(line.strip()))
                index[word_index].append(int(line.strip()))

    print("re", word, index)
    return word, index

def WriteOutput(outfile, cost, line1, line2, time, memory):
    with open(outfile, 'w') as f:
        f.write(str(cost) + "\n")
        f.write(line1 + "\n")
        f.write(line2 + "\n")
        f.write(str(time) + "\n")
        f.write(str(memory) + "\n")

def extensiont(string, index_li):
    # keys = list(string.keys())
    # print("keys", keys)
    word1 = string[0]
    word2 = string[1]
    # print("keys", word1, word2)
    for i in index_li[0]:
        word1 = word1[:i+1] + word1 + word1[i+1:]
    for j in index_li[1]:
        word2 = word2[:j + 1] + word2 + word2[j + 1:]
    # print("word", word1, word2)
    return word1, word2

string, index_li = ReadInput(inputfile)
line1, line2 = extensiont(string, index_li)
WriteOutput(outfile_b, 0, line1, line2, 0, 0)
