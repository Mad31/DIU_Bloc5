"""
Explorations for Sokoban.
Fill free to add new exploration code here.
"""

from numpy import deprecate
import pygame
from pygame.locals import *
import common as C
from utils import *
import queue
import heapq
from time import time
from math import sqrt
import networkx as nx
import matplotlib.pyplot as plt
from level import *


class DFS:
    """
    Classical Depth-First Search walkthrough of the level to discover what is 
    the "interior" and "exterior.
    """

    def __init__(self, level):
        self.level = level

    def search_floor(self, source):
        init_x, init_y = source

        # to remember which tiles have been visited or not
        mark = [[False for x in range(self.level.width)]
                for y in range(self.level.height)]

        def rec_explore(position):
            x, y = position
            if mark[y][x]:
                return

            # mark current position as visited
            mark[y][x] = True

            for d, (mx, my) in enumerate(C.DIRS):
                if self.level.is_wall((x+mx, y+my)):
                    continue

                rec_explore((x+mx, y+my))

        rec_explore(source)
        return mark

class Solveur :

    def __init__(self,level) :
        self.level = level
        self.Graph_Box = nx.DiGraph()
        self.Graph_Fille = nx.Graph()
        self.Graph_Etats = nx.DiGraph()
        position_joueur = self.level.player_position
        for x in range(1,len(self.level.map[0])-1) :
            for y in range(1,len(self.level.map)-1) :
                if self.level.mboxes[y][x] ==  True:
                    position_caisse = (x,y)
        self.association = {"0" : (position_joueur,position_caisse)}
        self.Graph_Etats.add_node("0",pos = (0,0))

    def set_nodes(self,graphe) :
        # Place les noeuds sur un graphe à) partir de la carte niveau
        for x in range(len(self.level.map[0])) :
            for y in range(len(self.level.map)) :
                if self.level.map[y][x] == 7 or self.level.map[y][x] == 3 or self.level.map[y][x] == 5:
                    graphe.add_node(str(x)+":"+str(y),pos=(x*4,-y*4))

    def set_edges(self,graphe) :
        # Place les aretes
        for x in range(1,len(self.level.map[0])-1) :
            for y in range(1,len(self.level.map)-1) :
                if self.level.map[y][x] == 7 or self.level.map[y][x] == 3 or self.level.map[y][x] == 5:
                    if (self.level.map[y][x+1] == 7  or self.level.map[y][x+1] == 3 or self.level.map[y][x+1] == 5) and self.level.map[y][x-1] !=1:
                        graphe.add_edge(str(x)+":"+str(y),str(x+1)+":"+str(y))
                    if (self.level.map[y][x-1] == 7 or self.level.map[y][x-1] == 3 or self.level.map[y][x-1] == 5) and self.level.map[y][x+1] !=1:
                        graphe.add_edge(str(x)+":"+str(y),str(x-1)+":"+str(y))
                    if (self.level.map[y-1][x] == 7 or self.level.map[y-1][x] == 3 or self.level.map[y-1][x] == 5) and self.level.map[y+1][x] !=1:
                        graphe.add_edge(str(x)+":"+str(y),str(x)+":"+str(y-1))
                    if (self.level.map[y+1][x] == 7 or self.level.map[y+1][x] == 3 or self.level.map[y+1][x] == 5) and self.level.map[y-1][x] !=1:
                        graphe.add_edge(str(x)+":"+str(y),str(x)+":"+str(y+1))

    def Cons_Graph_fille(self,graphe) :
        # Constructeur du graphe fille
        # On supprime le noeud où se trouve la caisse
        for x in range(1,len(self.level.map[0])-1) :
            for y in range(1,len(self.level.map)-1) :
                if self.level.mboxes[y][x] ==  True:
                    graphe.remove_node(str(x)+":"+str(y))

    def Cons_Graphe_Etat_Niveau(self,graphe_box,noeud_niveau) :
        compteur = 0
        # On récupere la position de la caisse
        depart_caisse = self.association[noeud_niveau][1]
        depart_caisse_chaine = str(depart_caisse[0])+":"+str(depart_caisse[1])
        # On construit le graphe fille
        self.set_nodes(self.Graph_Fille)
        self.set_edges(self.Graph_Fille)
        # position_fille = self.association[str(numero_niveau)+"-"+str(compteur)][0]
        # position_fille = str(position_fille[0]) + ":" + str(position_fille[1])
        self.Graph_Fille.remove_node(depart_caisse_chaine)
        # On cherche les chemins possibles pour la caisse à partir de sa position actuelle
        voisins = [n for n in graphe_box.neighbors(depart_caisse_chaine)]
        # Pour chaque voisin on cherche si la fille peut pousser la caisse
        for voisin in voisins :
            arrivee_caisse = (int(voisin.split(":")[0]),int(voisin.split(":")[1]))
            # On cherche où doit se positionner la fille pour pousser la caisse
            # La caisse se déplace vers la gauche ?
            if arrivee_caisse[0] == depart_caisse[0] - 1 and arrivee_caisse[1] == depart_caisse[1]:
                arrivee_fille = (depart_caisse[0]+1,depart_caisse[1])
                arrivee_fille_chaine = str(depart_caisse[0]+1)+":"+str(arrivee_caisse[1])
            # La caisse se déplace vers la droite ?
            if arrivee_caisse[0] == depart_caisse[0] + 1 and arrivee_caisse[1] == depart_caisse[1]:
                arrivee_fille = (depart_caisse[0])-1,depart_caisse[1]
                arrivee_fille_chaine = str(depart_caisse[0]-1)+":"+str(arrivee_caisse[1])
            # La caisse de déplace vers le bas ?
            if arrivee_caisse[1] == depart_caisse[1] + 1 and arrivee_caisse[0] == depart_caisse[0]:
                arrivee_fille = (depart_caisse[0],depart_caisse[1]-1)
                arrivee_fille_chaine = str(depart_caisse[0]) + ":" + str(depart_caisse[1]-1)
            # La caisse se déplace vers le haut ?
            if arrivee_caisse[1] == depart_caisse[1] - 1 and arrivee_caisse[0] == depart_caisse[0] :
                arrivee_fille = (depart_caisse[0],depart_caisse[1]+1)
                arrivee_fille_chaine = str(depart_caisse[0]) + ":" + str(depart_caisse[1] + 1)
            # On va maintenant chercher si la fille peut pousser la caisse
            depart_fille = self.association[noeud_niveau][0]
            depart_fille_chaine = str(depart_fille[0])+":"+str(depart_fille[1])
            # print ("la fille doit aller de ",depart_fille," à ",arrivee_fille)
            # si la fille est déjà au bon endroit pas la peine de chercher un chemin
            if depart_fille == arrivee_fille :
                # print("la fille est déjà en place, on ajoute un noeud")
                self.association[noeud_niveau+str(compteur)] = (depart_caisse,arrivee_caisse)
                self.Graph_Etats.add_node(noeud_niveau+str(compteur),pos=(-len(noeud_niveau)*3 + int(noeud_niveau) * 4 + compteur,-len(noeud_niveau)))
                self.Graph_Etats.add_edge(noeud_niveau,noeud_niveau+str(compteur))
                compteur += 1
            elif self.cherche_chemin(self.Graph_Fille,depart_fille_chaine,arrivee_fille_chaine) != None :
                # print("la fille n'est pas en place, on cherche un chemin")
                self.association[noeud_niveau+str(compteur)] = (depart_caisse,arrivee_caisse)
                self.Graph_Etats.add_node(noeud_niveau+str(compteur),pos=(-len(noeud_niveau)*3 + int(noeud_niveau) * 4 + compteur,-len(noeud_niveau)))
                self.Graph_Etats.add_edge(noeud_niveau,noeud_niveau+str(compteur))
                compteur += 1

    def Cons_Graphe_Etat(self,graphe_box,graphe_fille) :
        for x in range(1,len(self.level.map[0])-1) :
            for y in range(1,len(self.level.map)-1) :
                 if self.level.map[y][x] == 3 :
                     position_cible = (x,y)
        niveau = 2
        valeur = [i[1] for i in self.association.values()]
        self.Cons_Graphe_Etat_Niveau(graphe_box,"0")
        while position_cible not in valeur :
            liste_noeuds = [n for n in self.association.keys() if len(n) == niveau]
            for i in liste_noeuds :
                self.Cons_Graphe_Etat_Niveau(graphe_box,i)
            valeur = [i[1] for i in self.association.values()]
            niveau += 1
            print(niveau)
        for k, val in self.association.items(): 
            if position_cible == val[1]: 
                noeud_solution = k
        parcours_solution = []
        while noeud_solution != "0" :
            parcours_solution.append(self.association[noeud_solution])
            noeud_solution = list(self.Graph_Etats.predecessors(noeud_solution))[0]
        print (parcours_solution)
            
    def affichage(self,graphe) :
        node_pos=nx.get_node_attributes(graphe,'pos')
        color_map=[]
        color_map.append('blue')
        nx.draw_networkx(graphe, node_pos, node_size=700,node_color = color_map)
        plt.axis('off')
        plt.show()

    def cherche_chemin(self,graphe,depart,arrivee) :
        pile = [(depart,[depart])]
        chemin = []
        while len(pile) != 0:
            sommet,chemin = pile.pop()
            liste_nouveaux_sommets_voisins = [voisin for voisin in graphe.neighbors(sommet) if not(voisin in chemin)]
            for voisin in liste_nouveaux_sommets_voisins:
                if voisin == arrivee:
                    return chemin + [arrivee]
                pile.append((voisin,chemin + [voisin]))
        return None

    def cherche_tous_chemins(self,graphe,depart,arrivee):
        chemins = []
        pile = [(depart,[depart])]
        chemin = []
        while len(pile) != 0:
            sommet,chemin = pile.pop()
            liste_nouveaux_sommets_voisins = [voisin for voisin in graphe[sommet] if not(voisin in chemin)]
            for voisin in liste_nouveaux_sommets_voisins:
                if voisin == arrivee:
                    chemins.append(chemin + [arrivee])
                pile.append((voisin,chemin + [voisin]))
        # On trie les chemins du plus court au plus long
        chemins.sort(key=lambda item:len(item))
        return chemins

    
    
      

    







