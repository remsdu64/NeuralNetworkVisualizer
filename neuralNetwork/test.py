#!/usr/bin python3.6
# coding: utf-8
import MLP

# This line is for creating the neural network
#test = MLP.MLP((2, 16, 32, 64, 128, 256, 128, 1), True)
# This line is for loading th neural network
test = MLP.MLP()

nbrcouches, nbr, connecs = test.infos()


print("There are " + str(nbr) + " neurons in the brain of " + str(nbrcouches) +
      " layers including " + str(nbrcouches - 2) + " hidden layers")
print("Il y a " + str(connecs) + " connexions dans le cerveau")


data = [[[0, 0], [0]], [[1, 0], [0]], [[0, 1], [0]], [[1, 1], [1]], [[0.6, 0.8], [1]], [[0.7, 0.9], [1]]]
print("Apprentissage...")

erreur, temps = test.apprend(data, 0.1, 1, debug=False)
test.save()

result = test.execute([[1, 1], []])

print(result)
