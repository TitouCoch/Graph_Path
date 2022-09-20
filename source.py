# -*- coding: utf-8 -*-
"""
Created on Fri May 20 09:45:33 2022

@author: tcocheril001
"""

from graphics import *
import math
#Importation de la bibliothèque json
import json
#Importation des bibliothèques sin, cos, acos, pi 
from math import sin, cos, acos, pi


 
#Intégration des données dans un dictionnaire
with open('donneesbus.json') as mon_fichier:
    data = json.load(mon_fichier)
    

#Liste contenants le nom de tous les arrêts
noms_arrets = []
for arrets in data.keys():
    noms_arrets.append(arrets) 

#fonction qui permet d’associer le nom du sommet à un indice de noms_arrets
def nom(ind):
    return noms_arrets[ind]
    

#fonction qui permet d’associer l'indice de l’arrêt à son nom nom_som
def indice_som(nom_som):
        for i in range(len(noms_arrets)):
                if noms_arrets[i]==nom_som:
                    indice=i
                    return indice               
   
#fonction qui renvoie la latitude d’un arrêt nommé nom_som
def latitude(nom_som):
    return data[nom_som][0]

#fonction qui renvoie la longitude d’un arrêt nommé nom_som
def longitude(nom_som):
    return data[nom_som][1]

#fonction qui renvoie lla liste des voisins d’un arrêt nommé nom_som
def voisin(nom_som):
    return data[nom_som][2]

#creation de la liste d’adjacence grace a un dictionnaire dic_bus
dic_bus={}
for i in (noms_arrets):
    dic_bus[i]=voisin(i)

#creation de la matrice d’adjacence mat_bus grace a une liste de listes
mat_bus = []
for i in (noms_arrets):
    mat_bus.append([])
    for j in (noms_arrets):
        if j in voisin(i):
            mat_bus[indice_som(i)].append(1)
        else:
            mat_bus[indice_som(i)].append(0)   

      

#########################################################
# calcul de la distance entre deux points A et B dont #
# on connait la lattitude et la longitude #
#########################################################
def distanceGPS(latA,latB,longA,longB):
 # Conversions des latitudes en radians
 ltA=latA/180*pi
 ltB=latB/180*pi
 loA=longA/180*pi
 loB=longB/180*pi
 # Rayon de la terre en mètres (sphère IAG-GRS80)
 RT = 6378137
 # angle en radians entre les 2 points
 S = acos(round(sin(ltA)*sin(ltB) + cos(ltA)*cos(ltB)*cos(abs(loB-loA)),14))
 # distance entre les 2 points, comptée sur un arc de grand cercle
 return S*RT

#Fonction renvoyant la distance à vol d’oiseau entre les arrêts arret1 et arret2
def distarrets(arret1,arret2):
    return distanceGPS(latitude(arret1),latitude(arret2),longitude(arret1),longitude(arret2))
 
#Fonction renvoyant la distance à vol d’oiseau entre les les arrêts arret1 et arret2 si l'arc existe  
def distarc(arret1,arret2):
    if arret2 in voisin(arret1):
        return distanceGPS(latitude(arret1),latitude(arret2),longitude(arret1),longitude(arret2))
    else:
        return 0
    
   
#reprensentantation du graphe pondéré en une matrice
poids_bus=[]
for i in (noms_arrets):
    poids_bus.append([])
    for j in (noms_arrets):
        if distarc(i,j) !=0:
            poids_bus[indice_som(i)].append(distarc(i,j))
        else:
            poids_bus[indice_som(i)].append(float("inf"))

