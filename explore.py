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

class Solveur :

    def __init__(self,level) :
        self.level = level
        self.Graph_Box = nx.DiGraph()
        self.Graph_Fille = nx.Graph()
        self.Graph_Etats = nx.Graph()
        position_joueur = self.level.player_position
        for x in range(1,len(self.level.map[0])-1) :
            for y in range(1,len(self.level.map)-1) :
                if self.level.mboxes[y][x] ==  True:
                    position_caisse = (x,y)
        self.association = {0 : (position_joueur,position_caisse)}
        self.Graph_Etats.add_node("0",pos = (position_caisse))

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

    def affichage(self,graphe) :
        node_pos=nx.get_node_attributes(graphe,'pos')
        color_map=[]
        color_map.append('blue')
        nx.draw_networkx(graphe, node_pos, node_size=700,node_color = color_map)
        plt.axis('off')
        plt.show()

    def affiche_fille(self,graphe) :
        node_pos=nx.get_node_attributes(graphe,'pos')
        nx.draw_networkx(graphe, node_pos, node_size=700)
        plt.axis('off')
        plt.show()  

    def cherche_chemin(self,graphe,depart,arrivee) : 
        pile = [(depart,[depart])]
        chemin = []
        while len(pile) != 0:
            sommet,chemin = pile.pop()
            liste_nouveaux_sommets_voisins = [voisin for voisin in self.graphe[sommet] if not(voisin in chemin)]
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
            liste_nouveaux_sommets_voisins = [voisin for voisin in self.G[sommet] if not(voisin in chemin)]
            for voisin in liste_nouveaux_sommets_voisins:
                if voisin == arrivee:
                    chemins.append(chemin + [arrivee])
                pile.append((voisin,chemin + [voisin]))
        # On trie les chemins du plus court au plus long
        chemins.sort(key=lambda item:len(item))
        return chemins

    
    
      

    







