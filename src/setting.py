"""
Created on Sat May 28 12:50:01 2022
@author: Ivan Salle, Titouan Cocheril
"""


#-----------------------------------------------------------------------------------------------------------------
#IMPORTATION

import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import font as tkfont 
import time
from numpy import sqrt
from graphics import *
import math
#Importation de la bibliothèque json
import json
#Importation des bibliothèques sin, cos, acos, pi 
from math import sin, cos, acos, pi


#-----------------------------------------------------------------------------------------------------------------
#OUVERTURE DU FICHIER

#Intégration des données dans un dictionnaire
with open('donneesbus.json') as mon_fichier:
    data = json.load(mon_fichier)
    



#-----------------------------------------------------------------------------------------------------------------
#METHODES


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

#-----------------------------------------------------------------------------------------------------------------
#METHODES FENETRE


def maxlon():    #la longitude maximale
    max = -1000
    for a in noms_arrets:
        if longitude(a) > max:
            max = longitude(a)
    return(max)

def minlon():   #la longitude minamale
    min = float('inf')
    for a in noms_arrets:
        if longitude(a) < min:
            min = longitude(a)
    return(min)
    
def maxlat():   #la latitude maximale
    max = -1000
    for a in noms_arrets:
        if latitude(a) > max:
            max = latitude(a)
    return(max)
    
def minlat():   #la latitude minimale 
    min = float('inf')
    for a in noms_arrets:
        if latitude(a) < min:
            min = latitude(a)

    return(min)

def distLongitude():  #la distance en longitude
    return maxlon()-minlon()

def distLatitude():  #la distance en latitude 
    return maxlat()-minlat()


Ymetre = distanceGPS(minlat(),maxlat(),maxlon(),maxlon()) #la longueur en metre du coté en y de la fenetre 
Xmetre =  distanceGPS(maxlat(),maxlat(),maxlon(),minlon())#la longueur en metre du coté en x de la fenetre 
ratio = Ymetre/Xmetre   # le ratio de la fenetre 

def distanceLatMetre(i):  #renvoi la distance en metre entre un point et la latitude max
    return distanceGPS(latitude(i),maxlat(),longitude(i),longitude(i))
def distanceLonMetre(i):  #renvoi la distance en metre entre un point et la longitude max
    return distanceGPS(latitude(i),latitude(i),longitude(i),minlon())

margelatMetre = distanceGPS(43.552526+0.001,43.552526,-1.598933-0.001,-1.598933-0.001) #la marge en metre en latitude
margelonMetre = distanceGPS(43.552526+0.001,43.552526+0.001,-1.598933,-1.598933-0.001) #la marge en metre en longitude

marge = 20 # une marge de 20 pixel

# les mesures de la fenetre de placement des points en pixel
yFenetrePix = (ratio*900)-marge
xFenetrePix = 900-marge

margelatPix= xFenetrePix*margelatMetre/Xmetre    #la marge en pixel a pour les bords hautdroit et hautgauche
margelonPix= yFenetrePix*margelonMetre/Ymetre    


#-----------------------------------------------------------------------------------------------------------------
#POSITIONNEMENT DES SOMMETS  

dic_point={}
for i in noms_arrets: #les coordonées a et b en pixel + la marge
     a= xFenetrePix*distanceLonMetre(i)/Xmetre+margelonPix
     b= yFenetrePix*distanceLatMetre(i)/Ymetre+margelatPix
     dic_point[i]=Point(a,b)


#dictionnaire de cercles
dic_cercle={}
for i in noms_arrets:
    dic_cercle[i]= Circle(dic_point[i],4)
    
#dictionnaire de lignes
dic_ligne={}
for i in noms_arrets:        
    for v in voisin(i):
        key = i+"-"+v
        dic_ligne[key] = Line(dic_point[i],dic_point[v])

        

def ouvrir(sommet):
    dic_cercle[sommet].setFill(color_rgb(77,166,255))
     
    
def final(sommet):
    dic_cercle[sommet].setFill('red')
    
def clear():
    for i in noms_arrets:
        dic_cercle[i].setFill('white')

#-----------------------------------------------------------------------------------------------------------------
#PROGRAMME DE PARCOURS DE PLUS COURT CHEMINS

def dijkstra(depart,arrivee):
    #initialisation
    n = len(poids_bus)
    pred=[None]*n
    dist=[float("inf")]*n
    a_traiter=noms_arrets.copy() #liste de tout les sommets a traiter
    som=indice_som(depart) # on se place au depart
    ouvrir(nom(som))
    dist[indice_som(depart)]=0 # on met la distance du sommet de depart a 0
    while a_traiter != []: #tant que la liste des sommets a traitere n'est pas vide
        for i in voisin(nom(som)):
            if i in a_traiter:
                if dist[som] + poids_bus[som][indice_som(i)] < dist[indice_som(i)]: # si le chemin vers ce sommet voisin a partir du sommet est meilleur que l'ancien
                    if pred[som] != i: # evite les boucles (si le voisin n'est pas le predecesseceur du sommet)
                            dist[indice_som(i)] = dist[som] + poids_bus[som][indice_som(i)]
                            pred[indice_som(i)]=nom(som) #on met le sommet actuel comme predecesseur du sommet voisin
        som = indice_som(exctract_min(a_traiter, dist)) #on extrait le nouveau sommet de chemin de poids minimum qui est le nouveau sommet actuel
        ouvrir(nom(som))
        a_traiter.remove(nom(som)) # on enleve le sommet deja traité de la liste des sommets a traité
    liste = []
    liste.append(arrivee)
    a = arrivee # on se place sur le sommet d'arrivée
    fermer(a)
    while a != depart: # tant que l'on est pas arrivé au sommet de depart 
        liste.insert(0,pred[indice_som(a)]) #on insere le sommet au debut de la liste 
        a = pred[indice_som(a)] # on prend le predecesseceurs du sommet actuel
        fermer(a)
    return liste,dist[indice_som(arrivee)]

        
def getdistEstim(x,distance):      # fonction qui renvoie la distance du sommet x
    return distance[indice_som(x)]  

def Astar (depart,arrivee,vitesse):
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
                            ouvert.append(i)# on ajoute ce sommet voisin aux sommets ouverts
                            
                            pred[indice_som(i)] = nom(som) #on met le sommet actuel comme predecesseur du voisin 
                # on prend le meilleur nouveau sommet dans la liste des sommets ouverts
                ouvert=sorted(ouvert,key=lambda x: getdistEstim(x,dist_estim),reverse=True) # on tri la liste des sommets ovuerts par leurs distances estimées de la plus grande a la plus petite 
                som = indice_som(ouvert.pop()) # on definie le sommets de liste comme 
                time.sleep(vitesse*0.1)
                ferme.append(nom(som))
                ouvrir(nom(som))
        # cas d'une impasse
        else: # on elimine cette possibilté de chemin et on reviens au sommet precedent
            ferme.append(nom(som))
            som = indice_som(pred[som])
    #remplissage de la liste des predecesseurs du sommets arrivee
    liste = []
    liste.append(arrivee)
    a = arrivee
    final(a)
    while a != depart:
        liste.insert(0,pred[indice_som(a)])
        a = pred[indice_som(a)]
        final(a)
    return(liste,dist[indice_som(arrivee)])
    

#FLOYD WARSHALL
def FloydWarshall(arret_dep,arret_arriv,vitesse):

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
        ouvrir(nom(t))
        for u in range (len(noms_arrets)):
            for v in range (len(noms_arrets)):
                nouvellesDistances = mat_dist[u][t] + mat_dist[t][v]
                if nouvellesDistances < mat_dist[u][v]:
                    mat_dist[u][v] = nouvellesDistances
                    mat_pred[u][v] = mat_pred[t][v]
                    #time.sleep(vitesse*0.1)

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
        final(s)
        mat_result.append(s)
    mat_result.append(distance_final)  
    return mat_result                          




def Belmann(arret_dep,arret_arriv,vitesse):
    print(arret_dep)
    print(arret_arriv)
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
        ouvrir(nom(i))
        time.sleep(vitesse*0.1)
        #Boucle qui parcours tous les arrêts possible
        for j in noms_arrets:
            #Boucle qui parcours tous les voisins de l'arrêt traité
            for k in voisin(j):
                relachement(k, j)
                
    
    #Création de la matrice résultat
    liste_result=[arret_arriv]
    #Ajout du prédecesseur de l'arrêt d'arrivé
    pred_tmp = dist_pred[arret_arriv][1]
    final(pred_tmp)
    liste_result.insert(0,pred_tmp)
    #Boucle qui va ajouter tous les arrêts du chemin entre l'arrêt de départ et l'arrêt d'arrivée
    while pred_tmp!=arret_dep:
        pred_tmp=dist_pred[pred_tmp][1]
        final(pred_tmp)
        liste_result.insert(0,pred_tmp)
    
    #Ajout de la distance à la liste résultat
    liste_result.append(dist_pred[arret_arriv][0])
    return liste_result

def getdist(x,distance):
    return distance[indice_som(x)]

def dijkstra2(depart,arrivee,vitesse):
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
        time.sleep(vitesse*0.1)
        ouvrir(nom(som))
    liste = []
    liste.append(arrivee)
    a = arrivee
    final(a)
    while a != depart:
        liste.insert(0,pred[indice_som(a)])
        a = pred[indice_som(a)]
        final(a)
    return liste,dist[indice_som(arrivee)]





#Definition des fonction declanchées par l'evenement "motion" (souris bougée)

def motionDijkstra2(event,param):
    clear()
    x, y = event.x, event.y
    print("x",x,"y:",y)
    for sommet_actuel in noms_arrets:
        if distancePoint(dic_point[sommet_actuel],x,y) <= 4:
            dijkstra2(param[0],sommet_actuel,0)
            param[1].setText(sommet_actuel)
            time.sleep(3)
            
def motionAstar(event,param):
    clear()
    x, y = event.x, event.y
    print("x",x,"y:",y)
    for sommet_actuel in noms_arrets:
        if distancePoint(dic_point[sommet_actuel],x,y) <= 4:
            Astar(param[0],sommet_actuel,0)
            param[1].setText(sommet_actuel)
            time.sleep(2)
            
def motionBellman(event,param):
    clear()
    x, y = event.x, event.y
    print("x",x,"y:",y)
    for sommet_actuel in noms_arrets:
        if distancePoint(dic_point[sommet_actuel],x,y) <= 4:
            Belmann(param[0],sommet_actuel,0)
            param[1].setText(sommet_actuel)
            time.sleep(3)
            
def motionFloydWarshall(event,param):
    clear()
    x, y = event.x, event.y
    print("x",x,"y:",y)
    for sommet_actuel in noms_arrets:
        if distancePoint(dic_point[sommet_actuel],x,y) <= 4:
            FloydWarshall(param[0],sommet_actuel,0)
            param[1].setText(sommet_actuel)
            time.sleep(3)




def distancePoint(a,x,y):
    return sqrt((a.getX()-x)**2+(a.getY()-y)**2)

def defDepart(win,mesDepart):
    departCliqué = False
    while departCliqué == False:
        pointClick = win.getMouse()
        for sommet_actuel in noms_arrets:
            if distancePoint(dic_point[sommet_actuel],pointClick.getX(),pointClick.getY()) <= 4:
                departCliqué = True 
                mesDepart.setText(sommet_actuel)
                dic_cercle[sommet_actuel].setFill('green')
                return sommet_actuel
#-----------------------------------------------------------------------------------------------------------------
#BOUCLE AFFICHAGE CARTE
def main(programme,arretDep,arretArr,vitesse):
    A=900
    B=900*ratio
    win = GraphWin("Algorithme De Plus Court Chemin",A,B)
    image =Image(Point(A/2,B/2),"carte.png")
    image.draw(win)
    for i in noms_arrets:        
        c = dic_cercle[i] 
        c.setFill("white")
        c.draw(win)
        for v in voisin(i):
            key = i+"-"+v
            l=dic_ligne[key]
            l.setWidth(1)
            l.draw(win)
    if(programme=="Dijkstra"):
        dijkstra2(arretDep,arretArr,vitesse)
    if(programme=="A*"):
        Astar(arretDep,arretArr,vitesse)
    if(programme=="Bellman"):
        Belmann(arretDep,arretArr,vitesse)
    if(programme=="Floyd-Warshall"):
        FloydWarshall(arretDep,arretArr,vitesse)

    win.getMouse() # pause for click in window
    win.close()
    
def main2(programme):
    A=900     #la longueur haut de la fenetre   
    B=900*ratio     #la hauteur de la fenetre
    win = GraphWin("Algorithme De Plus Court Chemin",A,B)  
    image =Image(Point(A/2,B/2),"carte.png") #place la carte en fond
    image.draw(win)
    messageD = Text(Point(40,50), "DEPART:") # ecrit le nom du sommet dans l'angle
    messageD.setTextColor('white')
    mesDepart = Text(Point(100,50), "")
    mesDepart.setTextColor('white')
    mesDepart.draw(win)
    messageD.draw(win)
    messageA = Text(Point(40,70), "ARRIVEE:")
    messageA.setTextColor('white')
    mesArrivee = Text(Point(100,70), "")
    mesArrivee.setTextColor('white')
    mesArrivee.draw(win)
    messageA.draw(win)
    for i in noms_arrets:     #dessine chaque sommet en blanc    
        c = dic_cercle[i] 
        c.setFill("white")
        c.draw(win)
        for v in voisin(i): #dessine chaque lignes
            key = i+"-"+v
            l=dic_ligne[key]
            l.setWidth(1)
            l.draw(win)
    param=[None,None]  
    param[0] = defDepart(win,mesDepart) #les parametres des fonction d'algorithme
    param[1] = mesArrivee
    #Les evenement declanchés a chaque mouvement de souris
    if(programme=="Dijkstra"):
        print('oui')
        win.bind('<Motion>', lambda event, arg=param: motionDijkstra2(event, arg))
    if(programme=="A*"):
       win.bind('<Motion>', lambda event, arg=param: motionAstar(event, arg))
    if(programme=="Bellman"):
       win.bind('<Motion>', lambda event, arg=param: motionBellman(event, arg))
    if(programme=="FloydWarshall"):
        win.bind('<Motion>', lambda event, arg=param: motionFloydWarshall(event, arg))
    win.getMouse() # pause for click in window
    win.close()
    
    
    
    
#-----------------------------------------------------------------------------------------------------------------
# AFFICHAGE DU MENU
class ParcourDePlusCourtChemin(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        #Design des titres de fenêtre
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        
        
        #Le conteneur est l'endroit où nous allons empiler un tas de cadres
        #les uns sur les autres, puis celui que nous voulons visible
        #sera élevé au-dessus des autres
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            #Toutes les pages au même endroit ;
            #celui en haut de l'ordre d'empilement
            #sera celui qui est visible.
            frame.grid(row=0, column=0, sticky="nsew")

        #Initialise la fenêtre sur la page StartPage
        self.show_frame("StartPage")

    def show_frame(self, page_name):
        #Afficher un cadre pour le nom de page donné
        frame = self.frames[page_name]
        frame.tkraise()


#Fenêtre de menu
class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Titre
        label_titre=  tk.Label (self,text="Parcours de plus courts chemins",font=controller.title_font,fg='#0080ff')
        label_titre.pack(side="top", fill="x", pady=5)
        
        #Textes présentation programme
        label_texte=tk.Label (self,text="--------------------------")
        label_texte.pack()   
        label_texte=tk.Label (self,text="Les deux programmes ci-dessous \n affiche le parcour d'une liste \n d'arrêt suivant différent \n programmes  ")
        label_texte.pack()
        label_texte=tk.Label (self,text="--------------------------")
        label_texte.pack()   
        
        #Premier programme
        label_texte2=tk.Label (self,text="Choix du programme et des arrêts :")
        label_texte2.pack()
        bouton_Page1 = tk.Button(self,text="N°1",command=lambda: controller.show_frame("PageOne"),font=("Calibri", 12),fg="#0080ff")
        bouton_Page1.pack(padx=5)
        
        #Deuxième programme
        label_texte3=tk.Label (self,text="Choix sur la carte :")
        label_texte3.pack()
        bouton_Page2 = tk.Button(self,text="N°2",command=lambda: controller.show_frame("PageTwo"),font=("Calibri", 12),fg="#0080ff")
        bouton_Page2.pack(padx=10,pady=5)       
        
            

#Fenêtre premier programme sans évolution chronologique
class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Titre
        label_titre=  tk.Label (self,text="Parcours de plus courts chemins",font=controller.title_font,fg="#0080ff")
        label_titre.pack(side="top", fill="x",padx=10, pady=5)
        
        #Liste de choix programme
        list_programme = ["Floyd-Warshall", "Bellman", "Dijkstra", "A*"]
        Combo1 = ttk.Combobox(self, values=list_programme)
        Combo1.set("Choisi programme")
        Combo1.pack(padx=5, pady=5)
        
        
        #Liste de choix arrêt départ
        Combo2 = ttk.Combobox(self, values=noms_arrets)
        Combo2.set("Choisi arrêt dép")
        Combo2.pack(padx=5)
        
        #Liste de choix arrêt arrivée
        Combo3 = ttk.Combobox(self, values=noms_arrets)
        Combo3.set("Choisi arrêt arrivé")
        Combo3.pack(padx=5)
        
        #Scroll bar de choix de vitesse d'exécution
        label=  tk.Label (self,text="Choisi de la vitesse d'exécution")
        label.pack(side="top", fill="x")
        scrol_bar = Scale(self, from_=0, to=5, orient=HORIZONTAL)
        scrol_bar.pack(padx=5)
        
        
        #Bouton valider qui lance le programme
        bouton_V = tk.Button(self,text="Valider",command=lambda: main(Combo1.get(),Combo2.get(),Combo3.get(),scrol_bar.get()),font=("Calibri", 12),fg="#008000")
        bouton_V.pack(padx=5, pady=10)
        
        #Bouton précédent qui revient à la page de menu PageStart
        bouton_P = tk.Button(self,text="Précédent",command=lambda: controller.show_frame("StartPage"),font=("Calibri", 12),fg="#FF0000")
        bouton_P.pack(padx=5, pady=5,side=BOTTOM)


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        
        #Titre
        label_titre=  tk.Label (self,text="Parcours de plus courts chemins",font=controller.title_font,fg="#0080ff")
        label_titre.pack(side="top", fill="x",padx=10, pady=5)
        
        #Liste de choix programme
        list_luminosite = ["Floyd-Warshall", "Bellman", "Dijkstra", "A*"]
        Combop2 = ttk.Combobox(self, values=list_luminosite)
        Combop2.set("Choisi un programme")
        Combop2.pack(padx=5, pady=5) 
        
        
        
        
        #Bouton valider qui lance le programme
        bouton_V = tk.Button(self,text="Valider",command=lambda: main2(Combop2.get()),font=("Calibri", 12),fg="#008000")
        bouton_V.pack(padx=5, pady=10)
    
        #Bouton précédent qui revient à la page de menu PageStart
        bouton_P = tk.Button(self,text="Précédent",command=lambda: controller.show_frame("StartPage"),font=("Calibri", 12),fg="#FF0000")
        bouton_P.pack(padx=5, pady=5,side=BOTTOM)


#Boucle d'affichage et d'intération de la fenêtre
if __name__ == "__main__":
    app = ParcourDePlusCourtChemin()
    app.mainloop()





