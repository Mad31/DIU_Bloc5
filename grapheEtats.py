#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 09:29:54 2021

@author: a.rb
"""
import networkx as nx
from math import inf
import matplotlib.pyplot as plt

verbose=True
#dimensions du plateau de jeu
xmax= 3
ymax=3

positionInitiale=((1,1),(2,2)) #positions fille + caisse
positionC=(3,3) # position cible

dico={ ((xf,yf),(xc,yc)):"("+str(xf)+","+str(yf)+"/"+str(xc)+","+str(yc)+")" for xf in range(1,xmax+1) for yf in range(1,ymax+1) for xc in range(1,xmax+1) for yc in range(1,ymax+1) if (xc,yc)!=(xf,yf)}
sommets=[ value for keys, value in dico.items() if keys[0]!=keys[1]]

g=nx.DiGraph()
for s in sommets:
    g.add_node(s)

for keysB, valueB in dico.items():
    for keysE, valueE in dico.items():
        if keysB[1]==keysE[1] and (keysB[0][0]==keysE[0][0] and (keysB[0][1]==keysE[0][1]+1 or keysB[0][1]==keysE[0][1]-1)): #or keys1[0][1]+1==keys2[1][1]+1 or keys1[0][1]-1==keys2[1][1]-1 or keys1[0][0]+1==keys2[1][0]+1 or keys1[0][0]-1==keys2[1][0]-1:
            g.add_edge(valueB,valueE)
        elif keysB[1]==keysE[1] and (keysB[0][1]==keysE[0][1] and (keysB[0][0]==keysE[0][0]+1 or keysB[0][0]==keysE[0][0]-1)):
            g.add_edge(valueB,valueE)
        elif keysB[0][1]==keysB[1][1] and keysB[1][0]-keysB[0][0]==1 and keysE[0]==keysB[1] and keysE[1]==(keysB[1][0]+1,keysB[1][1]):
            g.add_edge(valueB,valueE)
        elif keysB[0][1]==keysB[1][1] and keysB[1][0]-keysB[0][0]==-1 and keysE[0]==keysB[1] and keysE[1]==(keysB[1][0]-1,keysB[1][1]):
            g.add_edge(valueB,valueE)
        elif keysB[0][0]==keysB[1][0] and keysB[1][1]-keysB[0][1]==1 and keysE[0]==keysB[1] and keysE[1]==(keysB[1][0],keysB[1][1]+1):
            g.add_edge(valueB,valueE)
        elif keysB[0][0]==keysB[1][0] and keysB[1][1]-keysB[0][1]==-1 and keysE[0]==keysB[1] and keysE[1]==(keysB[1][0],keysB[1][1]-1):
            g.add_edge(valueB,valueE)
        
if verbose :
    print("sommets :" , g.node())
    print("arcs :")
    for arc in g.edges():
        print(arc)
    print("dessin du graphe")
    options = {
      'node_color' : 'yellow',
      'node_size'  : 550,
      'edge_color' : 'tab:grey',
      'with_labels': True
    }
    plt.figure()
    nx.draw(g,**options)
    plt.show()


longueur=inf
chemin=[]
for keys, value  in dico.items() :
    if keys[1]==positionC :
        #print(keys)
        try :    
            cheminN=nx.astar_path(g,dico[positionInitiale],dico[keys])
            longueurN=len(cheminN)
            if longueurN<longueur:
                chemin=cheminN
                longueur=longueurN
        except:
            pass
print(chemin)