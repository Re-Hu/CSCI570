import time
import psutil

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper():
    start_time = time.time()
    basic_algorithm()
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    return time_taken

def extensiont(string):
    keys = list(string.keys())     # bug when two input word are the same!!!!!
    word1 = keys[0]
    word2 = keys[1]
    for i in string[word1]:
        word1 = word1[:i+1] + word1 + word1[i+1:]
    for j in string[word2]:
        word2 = word2[:j + 1] + word2 + word2[j + 1:]
    return word1, word2

delta = 30
alphas = [[0, 110, 48, 94],
          [110, 0, 118, 48],
          [48, 118, 0, 110],
          [94, 48, 110, 0]]
map_alphaIdx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}

def basic_algorithm(s1, s2):
    
    cost = 0    # cost of the alignment (integer)
    alignment_1 = ""    # first string alignment
    alignment_2 = ""    # second string alignment
    time_used = 0.0     # time in milliseconds (float)
    memory_used = 0.0   # memory in kilobytes (float)

    start_time = time.time()
    start_memory = process_memory()

    # basic sequence alignment algorithm - dynamic programming
    m = len(s1)
    n = len(s2)
    dp = [[0]*(n + 1) for i in range(m + 1)]
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
    time_used = (end_time - start_time)*1000

    # calculate memory taken
    end_memory = process_memory()
    memory_used = end_memory - start_memory

    # answer (minimum alignment cost) at dp[m][n]
    cost = dp[m][n]

    return cost, alignment_1, alignment_2, time_used, memory_used

if __name__ == '__main__':
    string = {'ACGT':[3,6,1,1,5,6,7,8,9,20], 'TACG':[1,2,0,4,3,2,0,5,6,17]}
    str1, str2 = extensiont(string)
    print("s1:", str1, "s2:", str2)
    results = basic_algorithm(str1, str2)
    print(results)
