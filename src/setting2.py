# -*- coding: utf-8 -*-
"""
Created on Tue Apr 19 14:13:04 2022

@author: tcocheril001
"""

#Importation de la bibliothèque json
import json
import numpy as np

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

#fonction qui renvoie la longitude d’un arrêt nommé nom_som
def voisin(nom_som):
    return data[nom_som][2]

#La liste d’adjacence par un dictionnaire dic_bus
def listeAdjacente():
    dic_bus={}
    for i in (noms_arrets):
        dic_bus[i]=voisin(i)
    return dic_bus

#La matrice d’adjacence par une liste de liste mat_bus
def matriceAdjacente():
    mat_bus = []
    for i in (noms_arrets):
      ligne = []
      for j in (noms_arrets):
         if j in voisin(i):
            ligne.append(1)
         else:
            ligne.append(0)       
            mat_bus.append(ligne)
    return mat_bus
print(matriceAdjacente())


      
#Importation des bibliothèques sin, cos, acos, pi 
from math import sin, cos, acos, pi
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
    
    
#Fonction reprensentant une matrice des poids du graphe pondéré

poids_bus=[]
for i in (noms_arrets):
    ligne = []
    for j in (noms_arrets):
        ligne.append(distarc(i,j))
    poids_bus.append(ligne)


  

  
#FLOYD WARSHALL
def FloydWarshall(arret_dep,arret_arriv):

#Matrice des prédecésseurs
    mat_pred = []
    for i in (noms_arrets):
      ligne = []
      for j in (noms_arrets):
         if j in voisin(i):
            ligne.append(indice_som(i))
         else:
            ligne.append(0)       
      mat_pred.append(ligne)

    
#Matrice des distances
    mat_dist=[]
    for i in (noms_arrets):
        ligne = []
        for j in (noms_arrets):
            if distarc(i,j) < 1:
                ligne.append(np.inf)
            else:
                ligne.append(distarc(i,j))
        mat_dist.append(ligne)

    
#Application de l'algorithme de Floyd Warshall 
    for t in range (len(noms_arrets)):
        for u in range (len(noms_arrets)):
            for v in range (len(noms_arrets)):
                nouvellesDistances = mat_dist[u][t] + mat_dist[t][v]
                if nouvellesDistances < mat_dist[u][v]:
                    mat_dist[u][v] = nouvellesDistances
                    mat_pred[u][v] = mat_pred[t][v]


#Extraction du chemin le plus court
    source = indice_som(arret_dep)
    destination = indice_som(arret_arriv)
    pile_result = [destination]
    while mat_pred[(source)][(destination)] != indice_som(arret_dep):
        pile_result.append(mat_pred[source][destination])
        destination = mat_pred[indice_som(arret_dep)][indice_som(arret_arriv)]

#Création de la matrice résultat
    mat_result = [arret_dep]
    distanceFinal=0
    

    
    while pile_result!=[]:
        s=nom(pile_result.pop(len(pile_result)-1))
        mat_result.append(s)

        
    for i in mat_result:
        for j in mat_result[1:len(mat_result)-1]:
            distanceFinal = distanceFinal + distarc(i,j) 
    mat_result.append(distanceFinal)  
    return mat_result                            
        
#print(FloydWarshall('NOVE','DURR'))



def Belmann(arret_dep,arret_arriv):
    n=len(noms_arrets)
    dist=[np.inf]*n
    pred=[None]*n
    dist[indice_som(arret_dep)]=0
    

    for i in range (len(poids_bus)-1):
        for j in range(len(noms_arrets)):
            for k in range(len(noms_arrets)):
                if dist[k] > dist[j] + distarc(nom(j),nom(k)):
                    dist[k] = dist[j] + distarc(nom(j),nom(k))
                    pred[k] = j

    print(dist)
    print(pred)
    mat_result=[]
    return mat_result

print(Belmann('NOVE', 'BAB'))

    

