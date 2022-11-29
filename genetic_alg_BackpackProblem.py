import pandas as pd
import random as rd

def mochila():
    bp = {'max_space':6, 'max_weight': 8, 'actual_space': 0, 'actual_weight': 0}
    return bp

def material():
    # ---------------------------------- building the list of material random
    dic_mat = {}
    for i in range(1,20):
        name = 'material_'+str(i)
        weight = 1+rd.random()                               # the range of weight is [1,2]
        val = rd.randrange(5)                            # the value is the range [1,5]
        dic_mat[name] = [weight, val]
    return dic_mat

def init_pob(size):

    size_pob = 6


    return 0

def main():
    # --------------------------------------------------- variables de ajuste
    prob_cruza = rd.random()
    prob_muta = rd.random()
    all_mat = material()
    backpack = mochila()

    max_weight = backpack['max_weight']
    max_space = backpack['max_space']

    mat_loaded = {}
    actual_weight = sum([i[0] for i in mat_loaded.values()])
    actual_value = sum([i[1] for i in mat_loaded.values()])
    # ---------------------------------------------------



