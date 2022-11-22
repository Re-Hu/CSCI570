import time
import sys
import psutil

penalty = 30
map_alphaIdx = {'A': 0, 'C': 1, 'G': 2, 'T': 3}
alpha = [[0, 110, 48, 94],
          [110, 0, 118, 48],
          [48, 118, 0, 110],
          [94, 48, 110, 0]]

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_used = int(memory_info.rss / 1024)
    return memory_used

def ReadInput(inputfile):
    with open(inputfile, 'r') as f:
        lines = f.readlines()
        word = []
        word_indes1 = -1
        indes1 = []
        string = ""
        for i in lines:
            line = i.strip()
            if not line.isdigit():
                word.append(line.strip())
                word_indes1 += 1
                indes1.append([])
            else:
                indes1[word_indes1].append(int(line.strip()))
    return word, indes1

def basic_algorithm(s1, s2):
    m = len(s1)
    n = len(s2)
    dp = [[0] * (n + 1) for i in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i * penalty
    for j in range(n + 1):
        dp[0][j] = j * penalty
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            alpha_ij = alpha[map_alphaIdx[s1[i - 1]]][map_alphaIdx[s2[j - 1]]]
            dp[i][j] = min(alpha_ij + dp[i - 1][j - 1], penalty + dp[i - 1][j], penalty + dp[i][j - 1])
            
    idx1 = m
    idx2 = n
    alignment_1 = ""  
    alignment_2 = "" 
    
    while (idx1>0 and idx2>0):
        al = alpha[map_alphaIdx[s1[idx1 - 1]]][map_alphaIdx[s2[idx2 - 1]]]
        if idx1 > 0 and idx2 > 0 and dp[idx1][idx2] == dp[idx1 - 1][idx2 - 1] + al:
            alignment_1 += s1[idx1 - 1]
            alignment_2 += s2[idx2 - 1]
            idx1 -= 1
            idx2 -= 1
        elif idx1 > 0 and dp[idx1][idx2] == penalty + dp[idx1 - 1][idx2]:
            alignment_1 += s1[idx1 - 1]
            alignment_2 += '_'
            idx1 -= 1
        elif idx2 > 0 and dp[idx1][idx2] == penalty + dp[idx1][idx2 - 1]:
            alignment_1 += '_'
            alignment_2 += s2[idx2 - 1]
            idx2 -= 1
    alignment_1 = alignment_1[::-1]
    alignment_2 = alignment_2[::-1]
    return alignment_1,alignment_2,dp[m][n]

def DC_helper(s1, s2):
    m = len(s1)+1
    n = len(s2)+1
    col = []
    col1= [0]*m
    col2 = [0]*m
    for i in range(m):
        col1[i] = penalty *i
    col.append(col1[-1])
    j=1
    while j<n:
        col2[0] = penalty*j
        for i in range(1, m):
            alpha_ij = alpha[map_alphaIdx[s2[j-1]]][map_alphaIdx[s1[i-1]]]
            col2[i] = min(penalty + col2[i-1],alpha_ij + col1[i-1], col1[i]+penalty)
        col.append(col2[-1])
        j+=1
        for i in range(len(col2)):
            col1[i] = col2[i]
    return col

def divide_conquer(s1, s2):
    m = len(s1)
    n = len(s2)
    if m<=2 or n<=2:
        return basic_algorithm(s1,s2)
    
    c1 = DC_helper(s1[m//2:][::-1],s2[::-1])[::-1]
    c2 = DC_helper(s1[:m//2],s2)
    minTotal=999999.0
    
    for i in range(len(c2)):
        s = c1[i]+c2[i]
        if s < minTotal:
            minTotal = s
            minId = i

    l1,l2,costl = divide_conquer(s1[:m//2], s2[:minId])
    r1,r2,cost2 = divide_conquer(s1[m//2:], s2[minId:])
    return  l1+r1, l2+r2 ,costl+cost2
 
def extensiont(string, indel1i):
    word1 = string[0]
    word2 = string[1]
    for i in indel1i[0]:
        word1 = word1[:i+1] + word1 + word1[i+1:]
    for j in indel1i[1]:
        word2 = word2[:j + 1] + word2 + word2[j + 1:]
    return word1, word2

def WriteOutput(outfile, cost, line1, line2, time, memory):
    with open(outfile, 'w') as f:
        f.write(str(cost) + "\n")
        f.write(line1 + "\n")
        f.write(line2 + "\n")
        f.write(str(time) + "\n")
        f.write("memory = "+str(memory) + "\n")

if __name__ == "__main__":
    inputfile = sys.argv[1]
    outfile = sys.argv[2]
    string, inde_li = ReadInput(inputfile)
    s1,s2 = extensiont(string, inde_li)
    start_time = time.time()
    start_memory = process_memory()
    d1,d2,cost = divide_conquer(s1,s2)
    end_memory = process_memory()
    end_time = time.time()
    total_time = (end_time - start_time)*1000
    memory_used = (end_memory - start_memory)
    WriteOutput(outfile,cost,d1,d2,total_time,memory_used)
