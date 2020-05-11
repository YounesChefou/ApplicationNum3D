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
#chaque point du cercle, représenter les points correspondants sur notre nouvelle dimension

#Nous allons sauvegarder les données dans un fichier txt pour les observer dans leur entiereté
np.savetxt('donnees.txt', donnees)

#Ce qu'il faut faire, c'est de d'abord recupérér les distances captées par le transducteur
#En partant du principe que la distance est le temps entre deux echos divisé par 340 m/s
#Chaque essai se repete toutes les 7000us et dure 86.5us

#Contrairement au projet en classe, le transducteur est ici fixe et ne descend pas de haut en bas
#Nous n'allons donc pas avoir un figure en 3D mais plutôt une tranche vue du dessus

#Pour recuperer les echos, il faut pouvoir les identifier, nous allons donc commencer par afficher la
#premiere ligne afin d'avoir une meilleure vision de l'acquisition

xvals = range(donnees.shape[1]);
plt.clf()
plt.plot(xvals,donnees[0])
plt.show()

#Voir fichier Acquisition_1.png
#Toutes les acquisitions ont le même profil, un pic correspondant à l'envoi de l'onde puis
#un pic plus faible correspondant à la reflexion de l'onde

#Proposition : "Normaliser" l'acquisition en determinant le seuil où un pic correspond à une reflexion
#de l'onde, toutes les valeurs inférieures seront mises à zéro et celles depassant le seul à 1
#A tester ce soir

# figure3D = np.empty((357, 357, 1384), dtype = float)
#
# for x in figure3D:
#     for y in x:
#         for z in y:
