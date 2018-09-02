#!/usr/local/bin/env python3.5
#coding: utf-8

import numpy as np
import fichiers
import time
import liens

fichiers.init()

tausApprentissage = 0.5

def sigmoid(x):
    return np.tanh(x)

def dsigmoid(x):
    return 1.0-x**2

def main(entrees, poids, sortieTemp):
    s=0
    for h in entrees:
        sortieTemp.append(h*poids[s])
        s+=1
    sortie = sigmoid(sum(sortieTemp))
    return sortie


class Ne():
    def __init__(self, poids = [0.5, 0.5]):
        self.poids = poids
        self.sortieTemp = []
        self.sortie = 0.0
        self.erreur = 0

        


def propagate_forward(reseau, data):
    ############ COUCHE D'ENTREE ############
    
    j = 0
    for i in reseau[0]:
        reseau[0][j].sortie = data[0][j]
        j+=1


    ############ COUCHES CACHEES ############
        
    n = 1
    cache = reseau[:]
    cache.pop(0)
    cache.remove(cache[-1])
    for i in cache:
        entreesTemp = []
        for h in reseau[n-1]:
            entreesTemp.append(h.sortie)
        for j in i:
            j.sortie = float(main(entreesTemp, j.poids, j.sortieTemp))
        n+=1

    ############ COUCHE DE SORTIE ############
    
    entrees = []

    sortie = []
    
    for w in reseau[-2]:
        entrees.append(w.sortie)
    for z in reseau[-1]:
        z.sortie = float(main(entrees, z.poids, z.sortieTemp))
        sortie.append(z.sortie)
    return sortie

"""
def propagate_backward(reseau, data):
    sortie = propagate_forward(reseau, data)
    ############ COUCHE DE SORTIE ############
    boucle = 0
    for i in reseau[-1]:
        i.erreur = dsigmoid(i.sortie)*(data[1][boucle]-i.sortie)
        boucle += 1

    cache = reseau[:]
    cache.remove(cache[-1])
    n=len(reseau)-1
    for couche in cache:
        h=0
        preCouche reseau(n+1)
        for preNeurone in preCouche:
            delta.append()
            h+=1
        for neurone in couche:
            neurone.erreur = float(neurone[n+1])
        n-=1
    print(cache)
"""

#reseau = [[Ne(), Ne()], [Ne(), Ne()], [Ne()]]
reseau = fichiers.load()

data = [[1, 1], [1]]

propagate_backward(reseau, data)
#print(reseau)
fichiers.save(reseau)
