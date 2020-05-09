import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
import tkinter
matplotlib.use('TkAgg')

donnees = np.load("arr_0.npy")
# print(donnees)
# print(donnees.shape)

#Tableau à 2 dimensions
#1ere dimension : n° essai
#2e dimension acquisition du transducteur

#Pour faire l'acquisition, l'objet a tourné sur lui même
#Chaque essai correspond donc au degré auquel l'objet était tourné => 360° une révolution
#Les acquisitions se faisaient donc de haut en bas
#Afin de pouvoir représenter la figure, on va utiliser mplot3d
#Mais pour cela, nous allons devoir rajouter une dimension

#Nous allons d'abord commencer par essayer de tracer un cercle
cercleX = np.empty(360, dtype = float)
cercleY = np.empty(360, dtype = float)

for i in range(0, 360):
    cercleX[i] = 5*np.cos(2*np.pi*(i/360))
    cercleY[i] = 5*np.sin(2*np.pi*(i/360))


# plt.clf()
# plt.plot(cercleX, cercleY)
# plt.show()

#Le principe de notre reconstruction est donc de parcourir notre cercle, et à
#chaque point du cercle, representer les 1384 points de la figure correspondant lié
# à ce point
#Nous allons sauvegarder les données dans un fichier txt pour les observer dans leur entiereté
np.savetxt('donnees.txt', donnees)
# figure3D = np.empty((357, 357, 1384), dtype = float)
#
# for x in figure3D:
#     for y in x:
#         for z in y:
