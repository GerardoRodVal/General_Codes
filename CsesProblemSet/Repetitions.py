'''
You are given a DNA sequence: a string consisting of characters A, C, G, and T. Your task is to find the longest
 repetition in the sequence. This is a maximum-length substring containing only one type of character.
'''

def repetitions(DNA):
    v = []
    c = 1
    for i,j in enumerate(DNA[:-1]):
        if j == DNA[i+1]:
            c += 1
        else:
            v.append(c)
            c = 1
    v.append(c)
    return max(v)
ADN = input()
print(repetitions(ADN))