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
inputfile = "input1.txt"
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
        word = {}
        string = ""
        for i in lines:
            line = i.strip()
            if not line.isdigit():
                word[line.strip()] = []
                string = line.strip()
            else:
                word[string].append(int(line.strip()))
    # print(word)
    return word

def WriteOutput(outfile, cost, line1, line2, time, memory):
    with open(outfile, 'w') as f:
        f.write(str(cost) + "\n")
        f.write(line1 + "\n")
        f.write(line2 + "\n")
        f.write(str(time) + "\n")
        f.write(str(memory) + "\n")

def extensiont(string):
    keys = list(string.keys())
    word1 = keys[0]
    word2 = keys[1]
    for i in string[word1]:
        word1 = word1[:i+1] + word1 + word1[i+1:]
    for j in string[word2]:
        word2 = word2[:j + 1] + word2 + word2[j + 1:]
    return word1, word2

w = ReadInput(inputfile)
line1, line2 = extensiont(w)
WriteOutput(outfile_b, 0, line1, line2, 0, 0)