def MinNumCoins(m):
    '''funcion que calcula el minimo cambio devuelto a partir de una cantidad'''
    minimos = [0]
    for i in range(1, m+1):
        m1 = (i - 5)
        m2 = (i - 4)
        m3 = (i - 1)
        l = [minimos[i] for i in [m1,m2,m3] if i >= 0]
        minimos.append(min(l)+1)
    return minimos[-1]
#print(MinNumCoins(8))

def DPChange(money, coins):
    minimos = [0]
    for i in range(1, money+1):
        minimo_i = MinNumCoins(i)
        for j in coins:
            if i >= j:
                if MinNumCoins(i - j) < minimo_i:
                    minimos.append(MinNumCoins(i-j)+1)
    min = minimos
    return min[money]
#print(DPChange(16, [50,25,20,10,5,1]))

import numpy as np
def ManhattanTourist(n, m, Down, Right):
    s = np.zeros((n,m))
    for i in range(1, n):
        s[0][i] = s[0][i-1]+(Down[0][i-1])

    for i in range(1, m):
        s[i][0] = s[i-1][0]+(Right[i-1][0])

    print(s)
    for i in range(1,n):
        for j in range(1,m):
            s[i][j] = max(s[j][i-1]+Down[j][i-1], s[j-1][i]+Right[j-1][i])
    return s
#Down = [[1, 0, 2, 4, 3], [4, 6, 5, 2, 1], [4, 4, 5, 2, 1], [5, 6, 8, 5, 3]]
#Right = [[3, 2, 4, 0], [3, 2, 4, 2], [0, 7, 3, 3], [3, 3, 0, 2], [1,3,2,2]]
#print(ManhattanTourist(4, 4, Down, Right))

def Global_Alignment(string1, string2):
        
    long1 = len(string1)
    long2 = len(string2)
    for i in range(1, long1):
        row = []
        for j in range(1, long2):
            row.append()

Global_Alignment('PLEASANTLY', 'MEANLY')