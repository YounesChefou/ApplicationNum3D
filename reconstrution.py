import streamlit as st
import os
from glob import glob

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import sys
import tkinter
matplotlib.use('TkAgg')

"""
# Reproduction de la forme d'un fantôme

"""

#Selection de fichier
def selection_fichier(dossier=os.getcwd()):
    fichiers = glob('*.npy')
    fichier_selectionne = st.selectbox('Selectionnez un fichier :', fichiers)
    if(fichier_selectionne):
        return os.path.join(dossier, fichier_selectionne)

nomFichier = selection_fichier()
if(nomFichier):
    st.write('Fichier selectionné : `%s`' % nomFichier)
    donnees = np.load(nomFichier)
    tAcq = 86.5e-6
    vOnde = 340
    tSec = tAcq/donnees.shape[1]

    

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
    # cercleX = np.empty(360, dtype = float)
    # cercleY = np.empty(360, dtype = float)
    #
    # for i in range(0, 360):
    #     cercleX[i] = 5*np.cos(2*np.pi*(i/360))
    #     cercleY[i] = 5*np.sin(2*np.pi*(i/360))


    # plt.clf()
    # plt.plot(cercleX, cercleY)
    # plt.show()

    #Le principe de notre reconstruction est donc de parcourir notre cercle, et à
    #chaque point du cercle, représenter les points correspondants sur notre nouvelle dimension

    #Nous allons sauvegarder les données dans un fichier txt pour les observer dans leur entiereté
    # np.savetxt('donnees.txt', donnees)

    #Ce qu'il faut faire, c'est de d'abord recupérér les distances captées par le transducteur
    #En partant du principe que la distance est le temps entre deux echos divisé par 340 m/s
    #Chaque essai se repete toutes les 7000us et dure 86.5us

    #Contrairement au projet en classe, le transducteur est ici fixe et ne descend pas de haut en bas
    #Nous n'allons donc pas avoir un figure en 3D mais plutôt une tranche vue du dessus

    #Pour recuperer les echos, il faut pouvoir les identifier, nous allons donc commencer par afficher la
    #premiere ligne afin d'avoir une meilleure vision de l'acquisition
    """
    ## Acquisitions

    """

    acq = st.slider("Acquisition n°", 0, donnees.shape[0]-1, 0, 1)

    xvals = range(donnees.shape[1]);
    # plt.clf()
    plt.plot(xvals,donnees[acq])
    st.pyplot()
    # plt.show()

    #Voir fichier Acquisition_1.png
    #Toutes les acquisitions ont le même profil, un pic correspondant à l'envoi de l'onde puis
    #un pic plus faible correspondant à la reflexion de l'onde

    #Proposition : "Normaliser" l'acquisition en determinant le seuil où un pic correspond à une reflexion
    #de l'onde, toutes les valeurs inférieures seront mises à zéro et celles depassant le seul à 1

    #Afin de trouver les pics, on va commencer par trouver le maximum à partir de 300
    #On va chercher ce maximum pour toutes les acquisitions pour ensuite trouver un seuil moyen

    # maximums = np.zeros(donnees.shape[0])
    # maximum = 0;
    # for j in range(0, donnees.shape[0]):
    #     for i in range(500, donnees.shape[1]):
    #         if(donnees[j][i] > maximum):
    #             maximum = donnees[j][i]
    #     maximums[j] = maximum
    #     maximum = 0

    # xvals = range(donnees.shape[0])
    # plt.clf()
    # plt.plot(xvals, maximums)
    # plt.show()

    #Sur l'image Maximums.png, on peut voir que les maximums ne sont pas constants pour toutes
    #les acquisitions avec des max à presque 2 et certains à 0.14, les pics à 2 sont dus au fait que
    #pour certaines acquisitions, l'ultrason était envoyé plus tard que les autres
    #Il nous faut detecter le premier ultrason et ensuite, detecter les pics étant supérieurs à
    #0.14

    #On va faire un tableau de dimensions 360x5
    #Donc dans chaque acquisition, on va recuperer l'indice correspondant au pic de l'ultrason et le
    #mettre au début de notre tableau, les 4 autres elements seront les pics correspondant aux reflexions des ondes
    #On commence donc à chercher les 4 autres pics 100 indices après notre pic d'ultrason

    # indPics = np.zeros((360, 5), dtype = int)
    # picUltra = False
    # seuilPicUltra = 1.45
    # seuilPicReflex = 0.14
    # k = 1
    # for i in range(0, donnees.shape[0]):
    #     for j in range(0, donnees.shape[1]):
    #         if(picUltra == False and donnees[i][j] > seuilPicUltra):
    #                 indPics[i][0] = j
    #                 picUltra = True
    #
    #         elif(picUltra == True and j > (indPics[i][0] + 100) and donnees[i][j] > seuilPicReflex and k < 5):
    #                 indPics[i][k] = j
    #                 k += 1
    #
    #     picUltra = False
    #     k = 1
    #
    # np.savetxt('indPics.txt', indPics) #On verifie si les données semblent cohérentes
    #
    # #On peut maintenant calculer les divers distances
    # #Le principe est simple, recuperer la difference entre l'indice d'un pic correspondant à la reflexion
    # #et l'indice de l'emission de l'ultrason, on la convertit en secondes et on la multiplie par la vitesse
    # #du son pour obtenir la distance
    #
    # distances = np.zeros((360, 4))
    # for i in range(0, indPics.shape[0]):
    #     for j in range(1, len(indPics[i])):
    #         diff = indPics[i][j] - indPics[i][0]
    #         t = diff*tSec
    #         distances[i][j-1] = (t*vOnde)/2
    #
    # np.savetxt('distances.txt', distances)
    #
    # #Maintenant que nous avons calculer les distances, nous pouvons commencer la représentation
    # #de la figure, nous allons donc parcourir le cercle et à chaque point, placer les points
    #
    # figureX = np.zeros((360, 4))
    # figureY = np.zeros((360, 4))
    #
    # for i in range(0, distances.shape[0]):
    #     for j in range(0, len(distances[i])):
    #         figureX[i][j] = distances[i][j]*np.cos(2*np.pi*(i/360))
    #         figureY[i][j] = distances[i][j]*np.sin(2*np.pi*(i/360))
    #
    #
    # #Nous pouvons maintenant representer cette figure sur un plot
    #
    # plt.clf()
    # plt.plot(figureX, figureY)
    # plt.show()

    #TODO: En verifiant le fichier indPics, on peut voir des données étranges (nbres negatifs par ex)
    #Solution : quand on instancie un tableau avec empty, les données qui ne sont pas remplies sont mises
    #à l'entier le plus grand ou le plus petit, on instancie avec zeros pour regler ce probleme

    #Ok, c'est faux hehe, l'acquisition commence à 13.5us et se termine à 100us, nos données
    #correspondent donc bien à 86.5us (100us - 13.5us), l'indice 0 est l'envoi des données
    #et le grand pic à plus de 2 est en fait le premier retour de l'echo, nous allons tester ça
    #Avec un tableau de distances ne prenant en compte que le premier pic

    #Vu que le seuil change souvent, on va plutôt prendre le pic maximum de l'acquisition

    def indPicMax(tab):
        ind = 0
        for i in range(0, tab.shape[0]):
            if(tab[i] > tab[ind]):
                ind = i
        return ind

    indPics2 = np.zeros(donnees.shape[0], dtype = int)
    picUltra = False
    seuilPicUltra = 0.3
    seuilPicReflex = 0.14
    k = 1
    for i in range(0, donnees.shape[0]):
        indPics2[i] = indPicMax(donnees[i])
        # for j in range(0, donnees.shape[1]):
            # if(donnees[i][j] > seuilPicUltra):
            #         indPics2[i] = j
            # elif(picUltra == True and j > (indPics2[i][0] + 100) and donnees[i][j] > seuilPicReflex and k < 5):
            #         indPics2[i][k] = j
            #         k += 1


    np.savetxt('indPics2.txt', indPics2) #On verifie si les données semblent cohérentes


    distances2 = np.zeros(donnees.shape[0])
    for i in range(0, indPics2.shape[0]):
            diff = indPics2[i]
            t = diff*tSec
            distances2[i] = (t*vOnde)/2

    np.savetxt('distances2.txt', distances2)

    #Maintenant que nous avons calculer les distances, nous pouvons commencer la représentation
    #de la figure, nous allons donc parcourir le cercle et à chaque point, placer les points

    figureX2 = np.zeros(distances2.shape[0])
    figureY2 = np.zeros(distances2.shape[0])

    for i in range(0, distances2.shape[0]):
            figureX2[i] = (5e-2-(distances2[i]*10))*np.cos(2*np.pi*(i/360))
            figureY2[i] = (5e-2-(distances2[i]*10))*np.sin(2*np.pi*(i/360))


    #Nous pouvons maintenant representer cette figure sur un plot

    # plt.clf()

    """
    ### Figure

    """

    plt.scatter(figureX2, figureY2)
    st.pyplot()
