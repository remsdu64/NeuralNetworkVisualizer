#!/usr/local/bin/env python3.5
#coding: utf-8

import numpy as np
import math
import random
import fichiers
import liens
import time

fichiers.init()
liens.init()

def sigmoid(x):
    return 1/(1 + math.e ** (-x))

def dsigmoid(x):
    return 1.0-x**2

def main(entrees, poids):
    s=0
    sortieTemp = []
    for h in entrees:
        sortieTemp.append(h*poids[s])
        s+=1
    #print(sortieTemp)
    sortie = sigmoid(sum(sortieTemp))
    return sortie

def antiMain(entrees, poids):
    s=0
    sortieTemp = []
    for h in entrees:
        sortieTemp.append(h*poids[s])
        s+=1
    #sortie = sigmoid(sum(sortieTemp))**(-1)
    sortie = 0.264
    return sortie

        


def propagate_forward(reseau, connexions, data):
    ############ COUCHE D'ENTREE ############
    
    boucle = 0
    for neurone in reseau[0]:
        neurone[2] = data[0][boucle]
        boucle+=1


    ############ COUCHES CACHEES ############
        
    numCouche = 1
    cache = reseau[:]
    cache.pop(0)
    cache.remove(cache[-1])

    
    for couche in cache:
        entreesTemp = []
        for neurone in couche:
            neuronesEntreesNom = []
            neuronesEntrees = []
            neuronesEntreesPoids = []
            for lien in connexions:
                if lien[1] == neurone[0]:
                    neuronesEntreesNom.append(lien[0])
                    neuronesEntreesPoids.append(lien[2])
            for neur in reseau[numCouche-1]:
                #print(neuronesEntreesNom)
                if neur[0] in neuronesEntreesNom:
                    neuronesEntrees.append(neur[2])
            neurone[2] = float(main(neuronesEntrees, neuronesEntreesPoids))
        numCouche+=1

    ############ COUCHE DE SORTIE ############
    
    entrees = []

    sortie = []

    for neurone in reseau[-1]:
        neuronesEntreesNom = []
        neuronesEntrees = []
        neuronesEntreesPoids = []
        for lien in connexions:
            if lien[1] == neurone[0]:
                neuronesEntreesNom.append(lien[0])
                neuronesEntreesPoids.append(lien[2])
        for y in reseau[-2]:
            if y[0] in neuronesEntreesNom:
                neuronesEntrees.append(y[2])
        neurone[2] = float(main(neuronesEntrees, neuronesEntreesPoids))
        sortie.append(neurone[2])
        return sortie


def propagate_backward(reseau, connexions, data, taux):
    sortie = propagate_forward(reseau, connexions, data)
    ############ COUCHES DE SORTIE ############
    i = 0
    for neurone in reseau[-1]:
      neurone[3] = data[1][i] - neurone[2]
      i+=1
    
    ############ COUCHES CAHEES + COUCHE D'ENTREE ############
    
    boucle = 0
    for i in reseau[-1]:
        i[3] = dsigmoid(i[2])*(data[1][boucle]-i[2])
        boucle += 1
    

    cache = reseau[:]
    cache.remove(cache[-1])
    n=len(cache)
    for couche in cache:
        h=0
        for neurone in couche:
            neuronesEntreesNom = []
            neuronesEntrees = []
            neuronesEntreesPoids = []
            for lien in connexions:
                if lien[0] == neurone[0]:
                    neuronesEntreesNom.append(lien[1])
                    neuronesEntreesPoids.append(lien[2])
            for neur in reseau[n-1]:
                if neur[0] in neuronesEntreesNom:
                    neuronesEntrees.append(neur[3])
            neur[3] = neur[2]  * (1-neur[2]) * main(neuronesEntrees, neuronesEntreesPoids)
        n-=1

    nouveauPoids = connexions[:]
    neuroneSortieLien = 0
    ############ MISE À JOUR ############
    n = 0
    for couche in reseau:
      for neurone in couche:
        i = 0
        for lien in connexions:
          if lien[0] == neurone[0]:
            for neur in reseau[n+1]:
              if neur[0] == lien[1]:
                nouveauPoids[i][2] = lien[2] + taux * neurone[2] * neur[3]
          i+=1
      n+=1
    return nouveauPoids






def propagate_generate(reseau, connexions, data):
    ############ COUCHES DE SORTIE ############
    i = 0
    for neurone in reseau[-1]:
      neurone[2] = data[i]
      i+=1
    
    ############ COUCHES CACHEES ############
        
    cache = reseau[:]
    cache.remove(cache[-1])
    n=len(cache)-1
    for couche in reversed(cache):
        h=0
        for neurone in couche:
            neuronesEntreesNom = []
            neuronesEntrees = []
            neuronesEntreesPoids = []
            for lien in connexions:
                if lien[0] == neurone[0]:
                    neuronesEntreesNom.append(lien[1])
                    neuronesEntreesPoids.append(lien[2])
            for neur in reseau[n+1]:
                print(neur[0])
                if neur[0] in neuronesEntreesNom:
                    neuronesEntrees.append(neur[3])
            neur[2] = antiMain(neuronesEntrees, neuronesEntreesPoids)
        n-=1

    neuroneSortieLien = []

    n = 0
    for neurone in reseau[0]:
      neuroneSortieLien.append(neurone[2])
    return neuroneSortieLien








def createReseau(infos):
    reseau = []
    n = 0
    nombre = 0
    for couche in infos:
        reseau.append([])
        for neurone in range(0, couche):
          neurTemp = []
          neurTemp.append(nombre)
          reseau[n].append([str(nombre), [], 0, 0])
          nombre += 1
        n+=1
    return reseau


def createLiens(reseau):
  connec = []
  n = 0
  cache = reseau[:]
  cache.remove(cache[-1])
  for couche in cache:
    for neurone in couche:
      for neurone2 in reseau[n+1]:
        connec.append([neurone[0], neurone2[0], random.uniform(-0.01, 0.01)])
    n+=1
  return connec
      

res = [2, 2, 1]
reseau = createReseau(res)

print("Il y a " + str(sum(res)) + " neurones dans le cerveau")
print("Il y a " + str(len(reseau)-1) + " couches dans le cerveau")

samples = [[[0, 0], [0]], [[1, 0], [1]], [[0, 1], [1]], [[1, 1], [0]]]


tauxApprentissage = 0.1
connexions = liens.load()
#connexions = createLiens(reseau)


####### APPRENTISSAGE ##########
nomApprentissages = 10000
depart = time.time()
for i in range(0, nomApprentissages):
  for data in samples:
    sortie = propagate_backward(reseau, connexions, data, tauxApprentissage)
    connexions = sortie
temp = time.time()
print("Apprentissage terminé en " + str(temp - depart) + " secondes")
liens.save(sortie)


dat = [[1, 0], [1]]
connex = liens.load()
#print(propagate_generate(reseau, connexions, [0]))
print(propagate_forward(reseau, connex, dat))
fichiers.save(reseau)
