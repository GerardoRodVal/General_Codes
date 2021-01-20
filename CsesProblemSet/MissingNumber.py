'''
You are given all numbers between 1,2,…,n except one. Your task is to find the missing number.
The first input line contains an integer n.
The second line contains n−1 numbers. Each number is distinct and between 1 and n (inclusive).
'''

def Missing(n, lista):
    l = sorted(lista)
    if l[-1] != n:
        return n
    x = 0
    for i in l:
        if x+1 == i:
            x += 1
        else:
            return x+1

n = int(input())
l = list(map(int, input().strip().split()))
print(Missing(n, l))