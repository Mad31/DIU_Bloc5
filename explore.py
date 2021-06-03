"""
Explorations for Sokoban.
Fill free to add new exploration code here.
"""

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

class Graph_Box :

    def __init__(self,level) :
        self.level = level
        self.G = nx.DiGraph()
    
    def set_nodes(self,graphe) :
        # print(self.level.map)
        for x in range(len(self.level.map[0])) :
            for y in range(len(self.level.map)) :
                if self.level.map[y][x] == 7 or self.level.map[y][x] == 3 or self.level.map[y][x] == 5:
                    graphe.add_node(str(x)+":"+str(y),pos=(x*4,-y*4))

    def set_edges(self,graphe) :
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
    def affichage(self) :
        node_pos=nx.get_node_attributes(self.G,'pos')
        chemins = self.cherche_tous_chemins()
        # print(chemins)
        color_map=[]
        if  chemins != [] :
            chemin = chemins[0]
            for node in self.G :
                if node in chemin :
                    color_map.append('red')
                else : 
                    color_map.append('blue')
        nx.draw_networkx(self.G, node_pos, node_size=700,node_color = color_map)
        plt.axis('off')
        plt.show()  

    def cherche_chemin(self) : 
        # On cherche les positions de départ et d'arrivée 
        for x in range(1,len(self.level.map[0])-1) :
            for y in range(1,len(self.level.map)-1) :
                if self.level.mboxes[y][x] ==  True:
                    depart = str(x)+":"+str(y)
                if self.level.map[y][x] == 3 :
                    arrivee = str(x)+":"+str(y)
        pile = [(depart,[depart])]
        chemin = []
        while len(pile) != 0:
            sommet,chemin = pile.pop()
            liste_nouveaux_sommets_voisins = [voisin for voisin in self.G[sommet] if not(voisin in chemin)]
            for voisin in liste_nouveaux_sommets_voisins:
                if voisin == arrivee:

                    return chemin + [arrivee]
                pile.append((voisin,chemin + [voisin]))
        return None

    def cherche_tous_chemins(self):
        nbre = 0
        # On cherche les positions de départ et d'arrivée 
        for x in range(1,len(self.level.map[0])-1) :
            for y in range(1,len(self.level.map)-1) :
                if self.level.mboxes[y][x] ==  True:
                    depart = str(x)+":"+str(y)
                if self.level.map[y][x] == 3 :
                    arrivee = str(x)+":"+str(y)
        chemins = []
        pile = [(depart,[depart])]
        chemin = []
        while len(pile) != 0:
            sommet,chemin = pile.pop()
            liste_nouveaux_sommets_voisins = [voisin for voisin in self.G[sommet] if not(voisin in chemin)]
            for voisin in liste_nouveaux_sommets_voisins:
                if voisin == arrivee:
                    chemins.append(chemin + [arrivee])
                pile.append((voisin,chemin + [voisin]))
            nbre += 1 
            print(nbre)
        chemins.sort(key=lambda item:len(item))
        return chemins
    
class Graph_Fille (Graph_Box):

    def __init__(self,level) :
        self.level = level
        self.G_fille = nx.Graph()

    def cons_Graph_fille(self,graphe) :
        # On supprime le noeud où se trouve la caisse
        for x in range(1,len(self.level.map[0])-1) :
            for y in range(1,len(self.level.map)-1) :
                if self.level.mboxes[y][x] ==  True:
                    graphe.remove_node(str(x)+":"+str(y))
    
    def affiche_fille(self) :
        node_pos=nx.get_node_attributes(self.G_fille,'pos')
        nx.draw_networkx(self.G_fille, node_pos, node_size=700)
        plt.axis('off')
        plt.show()  

    







