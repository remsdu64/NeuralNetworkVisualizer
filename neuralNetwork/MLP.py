#!/usr/local/bin/env python3.5
# coding: utf-8

class MLP():
    def __init__(self, network=None, link=False):
        import files
        import links
        files.init()
        links.init()
        if network:
            print("Creating network ...")
            self.network = self.createReseau(network)
            print("Creating links ...")
            self.links = self.createLiens()
        else:
            print("Loading network ...")
            self.network, self.links = files.load()
        """
        if link:
            print("Creating links ...")
            self.links = self.createLiens()
        else:
            print("Loading links ...")
            self.links = links.load()
        """
    
    def infos(self):
        nbrCouche = 0
        for couche in self.network:
            for neurone in couche:
                nbrCouche += 1
        return len(self.network), nbrCouche, len(self.links)

    def sigmoid(self, x):
        import math
        return 1 / (1 + math.e ** (-x))

    def dsigmoid(self, x):
        return 1.0 - x**2

    def main(self, entrees, poids):
        num = 0
        sortieTemp = []
        for h in entrees:
            sortieTemp.append(h * poids[num])
            num += 1
        # print(sortieTemp)
        output = self.sigmoid(sum(sortieTemp))
        return output

    def execute(self, data):
        # INPUT LAYER
        neuroneNumber = 0
        for neuron in self.network[0]:
            neuron[2] = data[0][neuroneNumber]
            neuroneNumber += 1

        # HIDDEN LAYERS

        layerNumber = 1
        cache = self.network[:]
        cache.pop(0)
        cache.remove(cache[-1])

        for layer in cache:
            for neuron in layer:
                neuronInputName = []
                neuronInput = []
                neuronInputWeight = []
                for lien in self.links:
                    if lien[1] == neuron[0]:
                        neuronInputName.append(lien[0])
                        neuronInputWeight.append(lien[2])
                for neur in self.network[layerNumber - 1]:
                    if neur[0] in neuronInputName:
                        neuronInput.append(neur[2])
                neuron[2] = float(
                    self.main(neuronInput, neuronInputWeight))
            layerNumber += 1

        # OUTPUT LAYER

        output = []
        for neurone in self.network[-1]:
            neuronesEntreesNom = []
            neuronesEntrees = []
            neuronesEntreesPoids = []
            for lien in self.links:
                if lien[1] == neurone[0]:
                    neuronesEntreesNom.append(lien[0])
                    neuronesEntreesPoids.append(lien[2])
            for y in self.network[-2]:
                if y[0] in neuronesEntreesNom:
                    neuronesEntrees.append(y[2])
            neurone[2] = float(
                self.main(neuronesEntrees, neuronesEntreesPoids))
            output.append(neurone[2])
        return output

    def propagate_backward(self, data, taux):
        erreur = []
        # OUTPUT LAYER
        i = 0
        for neurone in self.network[-1]:
            erreur.append(data[1][i] - neurone[2])
            neurone[3] = data[1][i] - neurone[2]
            i += 1

        # HIDDEN LAYERS + INPUT LAYER

        boucle = 0
        for i in self.network[-1]:
            i[3] = self.dsigmoid(i[2]) * (data[1][boucle] - i[2])
            boucle += 1

        cache = self.network[:]
        cache.remove(cache[-1])
        n = len(cache)
        for couche in cache:
            for neurone in couche:
                neuronesEntreesNom = []
                neuronesEntrees = []
                neuronesEntreesPoids = []
                for lien in self.links:
                    if lien[0] == neurone[0]:
                        neuronesEntreesNom.append(lien[1])
                        neuronesEntreesPoids.append(lien[2])
                for neur in self.network[n - 1]:
                    if neur[0] in neuronesEntreesNom:
                        neuronesEntrees.append(neur[3])
                neur[3] = neur[2] * (1 - neur[2]) * \
                    self.main(neuronesEntrees, neuronesEntreesPoids)
            n -= 1

        # UPDATE
        n = 0
        for couche in self.network:
            for neurone in couche:
                i = 0
                for lien in self.links:
                    if lien[0] == neurone[0]:
                        for neur in self.network[n + 1]:
                            if neur[0] == lien[1]:
                                self.links[i][2] = lien[2] + \
                                    taux * neurone[2] * neur[3]
                    i += 1
            n += 1
        return erreur

    def createReseau(self, infos):
        reseau = []
        n = 0
        nombre = 0
        for couche in infos:
            reseau.append([])
            for neurone in range(0, couche):
                neurTemp = []
                neurTemp.append(nombre)
                neur = [str(nombre), [], 0, 0]
                reseau[n].append(neur)
                nombre += 1
            n += 1
        return reseau

    def createLiens(self):
        import random
        connec = []
        n = 0
        cache = self.network[:]
        cache.remove(cache[-1])
        for couche in cache:
            for neurone in couche:
                for neurone2 in self.network[n + 1]:
                    connec.append([neurone[0], neurone2[0],
                                   random.uniform(-0.01, 0.01)])
            n += 1
        return connec

    def save(self):
        import files
        import links
        print("Saving network ...")
        files.save(self.network, self.links)

    def apprend(self, data, taux, repetitions, debug=False):
        import time
        debut = time.time()
        for tour in range(0, repetitions):
            deb = time.time()
            if debug:
                print("cycle d'apprentissage n°" + str(tour + 1))
            for exemple in data:
                erreur = self.propagate_backward(exemple, taux)
            """
            boucleEnvers = len(data)-1
            for exemple in data:
                erreur = self.propagate_backward(data[boucleEnvers], taux)
                boucleEnvers -= 1
            """
            if debug:
                print("fini en " + str(time.time() - deb) + " secondes")
        return erreur, time.time() - debut
