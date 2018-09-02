#!/usr/local/bin/env python3.5
#coding: utf-8

import numpy as np
import fichiers
import time
import liens
import math
import random

fichiers.init()
liens.init()

"""
def sigmoid(x):
    #return np.tanh(x)
    return 1 / (1 + math.exp(-x))
"""
def sigmoid(x):
    #return np.tanh(x)
    #print("Valeur : ")
    return 1/(1 + np.exp(-x))

"""
def dsigmoid(x):
    return 1.0-x**2
"""

def dsigmoid(x):
    return 1.0-x**2

def main(entrees, poids):
    s=0
    sortieTemp = []
    #print(entrees)
    for h in entrees:
        sortieTemp.append(h*poids[s])
        s+=1
    sortie = sigmoid(sum(sortieTemp))
    return sortie

def antiMain(entrees, poids):
    s=0
    sortieTemp = []
    #print(entrees)
    for h in entrees:
        sortieTemp.append(h*poids[s])
        s+=1
    sortie = sigmoid(sum(sortieTemp))**(-1)
    return sortie

class Ne():
    def __init__(self, identifiant):
        self.poids = []
        self.sortieTemp = []
        self.sortie = 0.0
        self.erreur = 0
        self.id = identifiant

        


def propagate_forward(reseau, connexions, data):
    ############ COUCHE D'ENTREE ############
    
    j = 0
    for neurone in reseau[0]:
        neurone.sortie = data[0][j]
        j+=1


    ############ COUCHES CACHEES ############
        
    n = 1
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
                if lien[1] == neurone.id:
                    neuronesEntreesNom.append(lien[0])
                    neuronesEntreesPoids.append(lien[2])
            for neur in reseau[n-1]:
                if neur.id in neuronesEntreesNom:
                    neuronesEntrees.append(neur.sortie)
                    #print(neur)
            neurone.sortie = float(main(neuronesEntrees, neuronesEntreesPoids))
        n+=1

    ############ COUCHE DE SORTIE ############
    
    entrees = []

    sortie = []

    for neurone in reseau[-1]:
        neuronesEntreesNom = []
        neuronesEntrees = []
        neuronesEntreesPoids = []
        for lien in connexions:
            if lien[1] == neurone.id:
                neuronesEntreesNom.append(lien[0])
                neuronesEntreesPoids.append(lien[2])
        for y in reseau[-2]:
            #for x in neuronesEntreesNom:
            if y.id in neuronesEntreesNom:
                neuronesEntrees.append(y.sortie)
        neurone.sortie = float(main(neuronesEntrees, neuronesEntreesPoids))
        sortie.append(neurone.sortie)
        return sortie


def propagate_backward(reseau, connexions, data, taux):
    sortie = propagate_forward(reseau, connexions, data)
    erreurTotal = []
    ############ COUCHES DE SORTIE ############
    i = 0
    for neurone in reseau[-1]:
      erreurTotal.append(data[1][i] - neurone.sortie)
      neurone.erreur = data[1][i] - neurone.sortie
      i+=1
    
    ############ COUCHES CAHEES + COUCHE D'ENTREE ############
    

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
                if lien[1] == neurone.id:
                    neuronesEntreesNom.append(lien[0])
                    neuronesEntreesPoids.append(lien[2])
            for neur in reseau[n-1]:
                if neur.id in neuronesEntreesNom:
                    neuronesEntrees.append(neur.erreur)
                    #print(neur)
            neur.erreur = neur.sortie  * (1-neur.sortie) * main(neuronesEntrees, neuronesEntreesPoids)
        n-=1

    nouveauPoids = connexions[:]
    neuroneSortieLien = 0
    ############ MISE À JOUR ############
    n = 0
    cache = reseau[:]
    cache.remove(cache[-1])
    for couche in cache:
      for neurone in couche:
        i = 0
        for lien in connexions:
          if lien[0] == neurone.id:
            for neur in reseau[n+1]:
              if neur.id == lien[1]:
                nouveauPoids[i][2] = lien[2] + taux * neurone.sortie * neur.erreur
                #neuroneSortieLien = lien[2] + taux * neurone.sortie * neur.erreur
                #break
          i+=1
      n+=1
    return nouveauPoids






def propagate_generate(reseau, connexions, data):
    #sortie = propagate_forward(reseau, connexions, data)
    ############ COUCHES DE SORTIE ############
    i = 0
    for neurone in reseau[-1]:
      neurone.sortie = data[i]
      i+=1
    
    ############ COUCHES CAHEES + COUCHE D'ENTREE ############

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
                if lien[0] == neurone.id:
                    neuronesEntreesNom.append(lien[1])
                    neuronesEntreesPoids.append(lien[2])
            for neur in reseau[n-1]:
                if neur.id in neuronesEntreesNom:
                    neuronesEntrees.append(neur.sortie)
                    #print(neur)
            neur.sortie = antiMain(neuronesEntrees, neuronesEntreesPoids)
        n-=1

    neuroneSortieLien = []
    ############ MISE À JOUR ############
    n = 0
    for neurone in reseau[0]:
      neuroneSortieLien.append(neurone.sortie)
    return neuroneSortieLien








def createReseau(infos):
    reseau = []
    n = 0
    nombre = 0
    for couche in infos:
        reseau.append([])
        for neurone in range(0, couche):
            reseau[n].append(Ne(nombre))
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
        connec.append([neurone.id, neurone2.id, random.uniform(-0.01, 0.01)])
        #connec.append([neurone.id, neurone2.id, 0])
    n+=1
  return connec
      

#reseau = [[Ne("1"), Ne("2")], [Ne("3"), Ne("4")], [Ne("5")]]
#res = [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 44, 42, 40, 38, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18, 16, 14, 12, 10, 8, 6, 4, 2, 1]
res = [2, 2, 1]
reseau = createReseau(res)
#reseau = fichiers.load()
print("Il y a " + str(sum(res)) + " neurones dans le cerveau")
print("Il y a " + str(len(reseau)-1) + " couches dans le cerveau")

#data = [[1, 1], [1]]
samples = [[[0, 0], [0]], [[1, 0], [0]], [[0, 1], [0]], [[1, 1], [1]]]
#samples = [[[0, 1], [0]], [[1, 1], [1]]]

"""connexions = [["1", "3", 0.01],["1", "4", -0.01],["2", "3", 0.005],["2", "4", -0.001],["3", "5", -0.05],["4", "5", 0.000000003]]
liens.save(connexions)
"""
"""
reseauConnect = reseau[:]
n = 0
for couche in reseau:
    print()
    print()
    i = 0
    for neurone in couche:
        print(reseauConnect)
        reseauConnect = reseauConnect[n].remove(reseauConnect[i])
        for ajoutCouche in reseauConnect:
            for ajoutNeurone in ajoutCouche:
                connexions.append([neurone.id, ajoutNeurone.id])
        i+=1
    reseauConnect.pop(0)
    n+=1
print(connexions)
"""

tauxApprentissage = 0.1
#connexions = liens.load()
connexions = createLiens(reseau)


####### APPRENTISSAGE ##########
nomApprentissages = 1000
depart = time.time()
for i in range(0, nomApprentissages):
  for data in samples:
    sortie = propagate_backward(reseau, connexions, data, tauxApprentissage)
    connexions = sortie
    #print(connexions)
temp = time.time()
#print("Apprentissage terminé en " + str(temp - depart) + " secondes")
liens.save(sortie)


data = [[1, 1], [1]]
connexions = liens.load()
#print(propagate_generate(reseau, connexions, [0]))
print(propagate_forward(reseau, connexions, data))
#print(liens.save(connexions))
#print(reseau)
fichiers.save(reseau)
