#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 13:25:32 2021

@author: a.rb
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 09:29:54 2021

@author: a.rb
"""
import networkx as nx
import matplotlib.pyplot as plt
#dimensions du plateau de jeu
xmax= 3
ymax=3
positionInitiale='(1,1/2,2)' # positions de départ fille + caisse
positionC=(3,3) #position de la cible

VERBOSE=True #Attention dessin du graphe particulierement lent

dico={ ((xf,yf),(xc,yc)):"("+str(xf)+","+str(yf)+"/"+str(xc)+","+str(yc)+")" for xf in range(1,xmax+1) for yf in range(1,ymax+1) for xc in range(1,xmax+1) for yc in range(1,ymax+1) if (xc,yc)!=(xf,yf)}
dicoinv={"("+str(xf)+","+str(yf)+"/"+str(xc)+","+str(yc)+")":((xf,yf),(xc,yc)) for xf in range(1,xmax+1) for yf in range(1,ymax+1) for xc in range(1,xmax+1) for yc in range(1,ymax+1) if (xc,yc)!=(xf,yf)}
sommets=[ value for keys, value in dico.items() if keys[0]!=keys[1]]


def ajout_arcs(g,sB:str,sE:str):
    sBTuple=dicoinv[sB]
    sETuple=dicoinv[sE]
   
    if sBTuple[1]==sETuple[1] and (sBTuple[0][0]==sETuple[0][0] and (sBTuple[0][1]==sETuple[0][1]+1 or sBTuple[0][1]==sETuple[0][1]-1)): #or keys1[0][1]+1==keys2[1][1]+1 or keys1[0][1]-1==keys2[1][1]-1 or keys1[0][0]+1==keys2[1][0]+1 or keys1[0][0]-1==keys2[1][0]-1:
        g.add_edge(sB,sE)
    elif sBTuple[1]==sETuple[1] and (sBTuple[0][1]==sETuple[0][1] and (sBTuple[0][0]==sETuple[0][0]+1 or sBTuple[0][0]==sETuple[0][0]-1)):
        g.add_edge(sB,sE)
    elif sBTuple[0][1]==sBTuple[1][1] and sBTuple[1][0]-sBTuple[0][0]==1 and sETuple[0]==sBTuple[1] and sETuple[1]==(sBTuple[1][0]+1,sBTuple[1][1]):
        g.add_edge(sB,sE)
    elif sBTuple[0][1]==sBTuple[1][1] and sBTuple[1][0]-sBTuple[0][0]==-1 and sETuple[0]==sBTuple[1] and sETuple[1]==(sBTuple[1][0]-1,sBTuple[1][1]):
        g.add_edge(sB,sE)
    elif sBTuple[0][0]==sBTuple[1][0] and sBTuple[1][1]-sBTuple[0][1]==1 and sETuple[0]==sBTuple[1] and sETuple[1]==(sBTuple[1][0],sBTuple[1][1]+1):
        g.add_edge(sB,sE)
    elif sBTuple[0][0]==sBTuple[1][0] and sBTuple[1][1]-sBTuple[0][1]==-1 and sETuple[0]==sBTuple[1] and sETuple[1]==(sBTuple[1][0],sBTuple[1][1]-1):
        g.add_edge(sB,sE)


def ajout(g,sommet):
    for s in g.nodes():
        if s!=sommet :
            ajout_arcs(g,sommet,s)
            ajout_arcs(g,s,sommet)
    
def recherche_chemin(graphe,positionInitiale:str,positionsfinales:set)->(bool,list):
    chemin=[]
    existe=False
    for s in positionsfinales :
        try : 
            chemin =nx.astar_path(graphe,positionInitiale,s)
            existe=True
        except :
            pass
    return existe,chemin
    
positionsf={((positionC[0]-1,positionC[1]),positionC), ((positionC[0]+1,positionC[1]),positionC),((positionC[0],positionC[1]-1),positionC),((positionC[0],positionC[1]+1),positionC)}
positionsfinales={dico[p] for p in positionsf if p in dico}
g=nx.DiGraph()
g.add_node(positionInitiale)

if VERBOSE :
    print("position initiale ",positionInitiale)
    print("cible ",positionC)
    print("positions finales ",positionsfinales)

for s in positionsfinales :
    g.add_node(s)
    ajout(g,s)

sommets=[ value for keys, value in dico.items() if keys[0]!=keys[1] and value != positionInitiale and value not in positionsfinales]
existe=False
while not existe and len(sommets)>0:
    existe,chemin = recherche_chemin(g,positionInitiale,positionsfinales)
    if existe :
        print("chemin : ",chemin)
    else :
        s=sommets[0]
        del sommets[0]
        g.add_node(s)
        ajout(g,s)
        
if VERBOSE :
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
    #nx.draw(g)
    #P.show()
