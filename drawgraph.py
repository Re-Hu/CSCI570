"""
CSCI 570 Filnal Project - drawgraph.py
Author: Xiaoyue Hu
get data from output files and draw graphs
"""
import os
import matplotlib.pyplot as plt

def getdata():
    path = os.getcwd()
    path_list = os.listdir(path)
    filelist = []
    for filename in path_list:
        # print("1", os.path.splitext(filename)[0])
        if "output" in os.path.splitext(filename)[0]:
            # print(filename)
            filelist.append(filename)
    print(filelist)
    return filelist

def generatedata(filelist):
    time = []
    memory = []
    mn = []
    for i in filelist:
        with open(i, 'r') as f:
            lines = f.readlines()
            # mn.append(len(lines[1].replace("_", "")))
            mn.append(lines[0].strip())
            time.append(lines[3].strip())
            memory.append(lines[4].strip())
    print(mn, time, memory)
    dict1 = dict(zip(mn, time))
    dict2 = dict(zip(mn, memory))
    # print(dict1, dict2)
    s = sorted(dict1)
    smooth_time = []
    smooth_memory = []
    # print(s)
    for j in s:
        smooth_time.append(dict1[j])
        smooth_memory.append(dict2[j])
    # print(smooth_time, smooth_memory)
    return s, smooth_memory, smooth_time

def draw(s, smooth_memory, smooth_time):
    plt.figure(1)
    plt.plot(s, smooth_time, color='tab:blue')
    # plt.plot(s, smoothAdvancedTime, color='tab:orange')
    plt.xlabel("m + n")
    plt.ylabel("CPU Time (s)")
    plt.legend(['Basic', 'Advanced'])
    plt.title("CPU Time vs problem size")
    # plt.gcf().subplots_adjust(left=0.3, top=0.91, bottom=0.09)
    plt.tight_layout()
    # plt.show()
    plt.savefig('CPUPlot.png')

    plt.figure(2)
    plt.plot(s, smooth_memory, color='tab:blue')
    # plt.plot(s, smoothAdvancedTime, color='tab:orange')
    plt.xlabel("m + n")
    plt.ylabel("Memory (MB)")
    plt.legend(['Basic', 'Advanced'])
    plt.title("Memory vs problem size")
    plt.tight_layout()
    # plt.gcf().subplots_adjust(left=0.15, top=0.91, bottom=0.09)
    # plt.show()
    plt.savefig('MemoryPlot.png')

f = getdata()
s, smooth_memory, smooth_time = generatedata(f)
draw(s, smooth_memory, smooth_time)