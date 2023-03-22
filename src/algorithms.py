# -*- coding: utf-8 -*-
"""
Created on Fri May 20 09:45:32 2022

@author: tcocheril001
"""

def exctract_min(sommets,distance):
    min = sommets[0]
    #print(min)
    #print(indice_som(min))
    for i in range(len(sommets)):
       # print(dist[indice_som(min)])
       # print(L[i])
       # print(indice_som(L[i]))
       # print(indice_som(min))
       if distance[indice_som(sommets[i])]<distance[indice_som(min)]:
           min = sommets[i]
    return min


def dijkstra(depart,arrivee):
    #initialisation
    n = len(poids_bus)
    pred=[None]*n
    dist=[float("inf")]*n
    a_traiter=noms_arrets.copy() #liste de tout les sommets a traiter
    som=indice_som(depart) # on se place au depart
    dist[indice_som(depart)]=0 # on met la distance du sommet de depart a 0
    while a_traiter != []: #tant que la liste des sommets a traitere n'est pas vide
        for i in voisin(nom(som)):
            if i in a_traiter:
                if dist[som] + poids_bus[som][indice_som(i)] < dist[indice_som(i)]: # si le chemin vers ce sommet voisin a partir du sommet est meilleur que l'ancien
                    if pred[som] != i: # evite les boucles (si le voisin n'est pas le predecesseceur du sommet)
                            dist[indice_som(i)] = dist[som] + poids_bus[som][indice_som(i)]
                            pred[indice_som(i)]=nom(som) #on met le sommet actuel comme predecesseur du sommet voisin
        som = indice_som(exctract_min(a_traiter, dist)) #on extrait le nouveau sommet de chemin de poids minimum qui est le nouveau sommet actuel
        a_traiter.remove(nom(som)) # on enleve le sommet deja traité de la liste des sommets a traité
    liste = []
    liste.append(arrivee)
    a = arrivee # on se place sur le sommet d'arrivée
    while a != depart: # tant que l'on est pas arrivé au sommet de depart 
        liste.insert(0,pred[indice_som(a)]) #on insere le sommet au debut de la liste 
        a = pred[indice_som(a)] # on prend le predecesseceurs du sommet actuel
    return liste,dist[indice_som(arrivee)]

        
def getdistEstim(x,distance):      # fonction qui renvoie la distance du sommet x
    return distance[indice_som(x)]  

def Astar (depart,arrivee):
    #initialisation
    n = len(poids_bus)
    pred=[None]*n
    dist=[float("inf")]*n
    dist_estim=[float("inf")]*n #liste des distances estimée
    som=indice_som(depart)
    ferme = []#liste des sommets visités
    ouvert = []#liste des sommets dont on a calculé la distance estimée
    dist[indice_som(depart)]=0 #on met la distance du sommet de depart a 0
    ferme.append(depart)
    while nom(som) != arrivee: #tant que le sommets actuel n'est pas le sommet d'arrivée
        if voisin(nom(som)) != []: #si le sommet a des voisins
                for i in voisin(nom(som)):#on estime les longeurs de chaque voisins du sommets actuel
                    if i not in ferme:# si le voisin n'est pas dans la liste des sommets fermé
                        if i not in ouvert or dist[indice_som(i)]>dist[som] + poids_bus[som][indice_som(i)]: #si on ne l'a pas encore ouvert(calcul de dist_estim) ou si le nouveau chemin est meilleur que l'ancien
                            dist[indice_som(i)] = dist[som] + poids_bus[som][indice_som(i)] #on met a jour la distance pour aller a i avec la distance du sommet actuel
                            dist_estim[indice_som(i)] = dist[indice_som(i)] + distarrets(i,arrivee) # on calcul la distance estimé avec la distance du sommets actuel + la distance pour aller du sommet actuel au voisin + la distance du voisin au somemt d'arrivée
                            ouvert.append(i) # on ajoute ce sommet voisin aux sommets ouverts
                            pred[indice_som(i)] = nom(som) #on met le sommet actuel comme predecesseur du voisin 
                # on prend le meilleur nouveau sommet dans la liste des sommets ouverts
                ouvert=sorted(ouvert,key=lambda x: getdistEstim(x,dist_estim),reverse=True) # on tri la liste des sommets ovuerts par leurs distances estimées de la plus grande a la plus petite 
                som = indice_som(ouvert.pop()) # on definie le sommets de liste comme 
                dic_cercle[i].setFill("red")
                ferme.append(nom(som))     
        # cas d'une impasse
        else: # on elimine cette possibilté de chemin et on reviens au sommet precedent
            ferme.append(nom(som))
            som = indice_som(pred[som])
    #remplissage de la liste des predecesseurs du sommets arrivee
    liste = []
    liste.append(arrivee)
    a = arrivee
    while a != depart:
        liste.insert(0,pred[indice_som(a)])
        a = pred[indice_som(a)]
    return(liste,dist[indice_som(arrivee)])


    

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
    #print(mat_pred)


#Matrice des distances
    mat_dist=[]
    for i in (noms_arrets):
        ligne = []
        for j in (noms_arrets):
            if distarc(i,j) < 1:
                ligne.append(float("inf"))
            else:
                ligne.append(distarc(i,j))
        mat_dist.append(ligne)
    #print(mat_dist)

    
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
    pile_result = [arret_arriv]
    distance_final=0
    while nom(destination)!=arret_dep:
        x=mat_pred[source][destination]
        pile_result.append(nom(x))
        y=mat_dist[x][destination]
        distance_final=distance_final+y
        destination=x
               
#Création de la matrice résultat
    mat_result = []
    while pile_result!=[]:
        s=pile_result.pop(len(pile_result)-1)
        mat_result.append(s)
        dic_cercle[s].setFill("red")
    mat_result.append(distance_final)  
    return mat_result                            
        
#print(FloydWarshall('NOVE','FEMM'))




def Belmann(arret_dep,arret_arriv):
    
    #Création d'un dictionnaire contenant pour clé le nom des arrêts, pour première valeur 
    #la distance entre les arrêts en partant du premier arrêt
    #comme deuxième valeur le prédécesseur
    #On attribuera à la valeur de départ la distance 0
    dist_pred={arrets: [float('inf'), None] for arrets in noms_arrets}
    dist_pred[arret_dep][0] = 0
    
    #Fonction de relachement d'un arrêt
    def relachement(a, b):
        arret1=a
        arret2=b
        if dist_pred[arret2][0] > dist_pred[arret1][0] + distarc(arret1, arret2):
            dist_pred[arret2][0] = dist_pred[arret1][0] + distarrets(arret1, arret2)
            dist_pred[arret2][1] = arret1

    #Boucle allant de 0 à 464 (autant de tours de boucles que d'arrêts)
    for i in range(0, len(poids_bus)-1):
        #Boucle qui parcours tous les arrêts possible
        for j in noms_arrets:
            #Boucle qui parcours tous les voisins de l'arrêt traité
            for k in voisin(j):
                relachement(k, j)
    
    #Création de la matrice résultat
    liste_result=[arret_arriv]
    #Ajout du prédecesseur de l'arrêt d'arrivé
    pred_tmp = dist_pred[arret_arriv][1]
    liste_result.insert(0,pred_tmp)
    #Boucle qui va ajouter tous les arrêts du chemin entre l'arrêt de départ et l'arrêt d'arrivée
    while pred_tmp!=arret_dep:
        pred_tmp=dist_pred[pred_tmp][1]
        liste_result.insert(0,pred_tmp)
    
    #Ajout de la distance à la liste résultat
    liste_result.append(dist_pred[arret_arriv][0])
    return liste_result

def getdist(x,distance):
    return distance[indice_som(x)]

def dijkstra2(depart,arrivee):
    n = len(poids_bus)
    pred=[None]*n
    dist=[float("inf")]*n
    dist[indice_som(depart)]=0
    a_traiter=noms_arrets.copy()
    som=indice_som(depart)
    while a_traiter != []:
        for i in  voisin(nom(som)):
            if i in a_traiter:
                if dist[som] + poids_bus[som][indice_som(i)] < dist[indice_som(i)]:
                    if pred[som] != i:# evite les boucles
                            dist[indice_som(i)] = dist[som] + poids_bus[som][indice_som(i)]
                            pred[indice_som(i)]=nom(som)
        a_traiter=sorted(a_traiter,key=lambda x: getdist(x,dist),reverse=True)
        som = indice_som(a_traiter.pop())#on enleve le sommet de meilleur chemin en haut de la queue de priorité
    liste = []
    liste.append(arrivee)
    a = arrivee
    while a != depart:
        liste.insert(0,pred[indice_som(a)])
        a = pred[indice_som(a)]
    return liste,dist[indice_som(arrivee)]