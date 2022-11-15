import time
import psutil
import sys


def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss / 1024)
    return memory_consumed


def time_wrapper():
    start_time = time.time()
    basic_algorithm()
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
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


delta = 30
alphas = [[0, 110, 48, 94],
          [110, 0, 118, 48],
          [48, 118, 0, 110],
          [94, 48, 110, 0]]
map_alphaIdx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}


def basic_algorithm(s1, s2):
    cost = 0  # cost of the alignment (integer)
    alignment_1 = ""  # first string alignment
    alignment_2 = ""  # second string alignment
    time_used = 0.0  # time in milliseconds (float)
    memory_used = 0.0  # memory in kilobytes (float)

    start_time = time.time()
    start_memory = process_memory()

    # basic sequence alignment algorithm - dynamic programming
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for i in range(m + 1)]
    print("m:", m, "n:", n)

    # base cases
    for i in range(m + 1):
        dp[i][0] = i * delta
    for j in range(n + 1):
        dp[0][j] = j * delta

    # bottom-up pass: find min alignment cost
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            alpha_ij = alphas[map_alphaIdx[s1[i - 1]]][map_alphaIdx[s2[j - 1]]]
            dp[i][j] = min(alpha_ij + dp[i - 1][j - 1], delta + dp[i - 1][j], delta + dp[i][j - 1])

    # top-down pass: find alignment strings
    idx1 = m
    idx2 = n
    while idx1 > 0 or idx2 > 0:
        alpha = alphas[map_alphaIdx[s1[idx1 - 1]]][map_alphaIdx[s2[idx2 - 1]]]
        if idx1 > 0 and idx2 > 0 and dp[idx1][idx2] == dp[idx1 - 1][idx2 - 1] + alpha:
            alignment_1 += s1[idx1 - 1]
            alignment_2 += s2[idx2 - 1]
            idx1 -= 1
            idx2 -= 1
        elif idx1 > 0 and dp[idx1][idx2] == delta + dp[idx1 - 1][idx2]:
            alignment_1 += s1[idx1 - 1]
            alignment_2 += '_'
            idx1 -= 1
        elif idx2 > 0 and dp[idx1][idx2] == delta + dp[idx1][idx2 - 1]:
            alignment_1 += '_'
            alignment_2 += s2[idx2 - 1]
            idx2 -= 1
    alignment_1 = alignment_1[::-1]
    alignment_2 = alignment_2[::-1]

    # calculate time taken
    end_time = time.time()
    time_used = (end_time - start_time) * 1000

    # calculate memory taken
    end_memory = process_memory()
    memory_used = end_memory - start_memory

    # answer (minimum alignment cost) at dp[m][n]
    cost = dp[m][n]

    return cost, alignment_1, alignment_2, time_used, memory_used


if __name__ == '__main__':
    inputfile = sys.argv[1]
    outfile = sys.argv[2]
    print("input", inputfile, outfile)
    string, index_li = ReadInput(inputfile)
    str1, str2 = extensiont(string, index_li)
    # str1, str2 = extensiont(string)
    # print("s1:", str1, "s2:", str2)
    results = basic_algorithm(str1, str2)
    cost, alignment_1, alignment_2, time_used, memory_used = basic_algorithm(str1, str2)
    WriteOutput(outfile, cost, alignment_1, alignment_2, time_used, memory_used)
