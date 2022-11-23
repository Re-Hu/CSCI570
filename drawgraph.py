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
    filelist_b = []
    filelist_e = []
    for filename in path_list:
        # print("1", os.path.splitext(filename)[0])
        if "outputbasic" in os.path.splitext(filename)[0]:
            # print(filename)
            filelist_b.append(filename)
        if "outputefficient" in os.path.splitext(filename)[0]:
            # print(filename)
            filelist_e.append(filename)
    # print(filelist_b)
    return filelist_b, filelist_e

def generatedata(filelist_b, filelist_e):
    time = []
    memory = []
    mn = []
    time_e = []
    memory_e = []
    mn_e = []
    for i in filelist_b:
        with open(i, 'r') as f:
            lines = f.readlines()
            mn.append(len(lines[1].strip().replace("_", "")) + len(lines[2].strip().replace("_", "")))
            time.append(round(float(lines[3].strip()), 4))
            memory.append(int(lines[4].strip()))
    print(mn, memory, time)
    for i in filelist_e:
        with open(i, 'r') as f:
            lines = f.readlines()
            mn_e.append(len(lines[1].strip().replace("_", "")) + len(lines[2].strip().replace("_", "")))

            time_e.append(round(float(lines[3].strip()), 4))
            memory_e.append(int(lines[4].strip()))
    # print("mn_e", mn_e, memory_e, time_e)

    dict1 = dict(zip(mn, time))
    dict2 = dict(zip(mn, memory))
    dict3 = dict(zip(mn_e, time_e))
    dict4 = dict(zip(mn_e, memory_e))
    # print("dict4", dict4)
    s = sorted(dict1)
    s2 = sorted(dict3)
    # print(dict1, dict2)
    smooth_time_e = []
    smooth_memory_e = []
    smooth_time = []
    smooth_memory = []
    print("s", dict1, dict3)
    for j in s:
        smooth_time.append(dict1[j])
        smooth_memory.append(dict2[j])
        smooth_time_e.append(dict3[j])
        smooth_memory_e.append(dict4[j])
    print(mn_e, time_e, memory_e)

    return s, smooth_memory, smooth_time, smooth_memory_e, smooth_time_e

def draw(s, smooth_memory, smooth_time, smooth_memory_e, smooth_time_e):
    plt.figure(1)
    plt.plot(s, smooth_time, color='tab:blue')
    plt.plot(s, smooth_time_e, color='tab:orange')
    plt.xlabel("m + n")
    plt.ylabel("CPU Time (MS)")
    plt.legend(['Basic', 'Advanced'])
    plt.title("CPU Time vs problem size")
    # plt.gcf().subplots_adjust(left=0.3, top=0.91, bottom=0.09)
    plt.tight_layout()
    # plt.show()
    plt.savefig('CPUPlot.png')

    plt.figure(2)
    plt.plot(s, smooth_memory, color='tab:blue')
    plt.plot(s, smooth_memory_e, color='tab:orange')
    plt.xlabel("m + n")
    plt.ylabel("Memory (MB)")
    plt.legend(['Basic', 'Advanced'])
    plt.title("Memory vs problem size")
    plt.tight_layout()
    # plt.gcf().subplots_adjust(left=0.15, top=0.91, bottom=0.09)
    # plt.show()
    plt.savefig('MemoryPlot.png')

file_basic, file_ef = getdata()
s, smooth_memory, smooth_time, smooth_memory_e, smooth_time_e = generatedata(file_basic, file_ef)
draw(s, smooth_memory, smooth_time, smooth_memory_e, smooth_time_e)