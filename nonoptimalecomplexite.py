#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 22:32:55 2021

@author: a.rb
"""

import networkx as nx
#import pylab as P
import matplotlib.pyplot as plt
#dimensions du plateau de jeu
import time as time





def ajout_arcs(g,sB:str,sE:str,dicoinv):
    sBTuple=dicoinv[sB]
    sETuple=dicoinv[sE]
   
    if sBTuple[1]==sETuple[1] and (sBTuple[0][0]==sETuple[0][0] and (sBTuple[0][1]==sETuple[0][1]+1 or sBTuple[0][1]==sETuple[0][1]-1)): #or keys1[0][1]+1==keys2[1][1]+1 or keys1[0][1]-1==keys2[1][1]-1 or keys1[0][0]+1==keys2[1][0]+1 or keys1[0][0]-1==keys2[1][0]-1:
        g.add_edge(sB,sE)
        #print("ajout1",sB,sE)
    elif sBTuple[1]==sETuple[1] and (sBTuple[0][1]==sETuple[0][1] and (sBTuple[0][0]==sETuple[0][0]+1 or sBTuple[0][0]==sETuple[0][0]-1)):
        g.add_edge(sB,sE)
        #print("ajout2",sB,sE)
    elif sBTuple[0][1]==sBTuple[1][1] and sBTuple[1][0]-sBTuple[0][0]==1 and sETuple[0]==sBTuple[1] and sETuple[1]==(sBTuple[1][0]+1,sBTuple[1][1]):
        g.add_edge(sB,sE)
        #print("ajout3",sB,sE)
    elif sBTuple[0][1]==sBTuple[1][1] and sBTuple[1][0]-sBTuple[0][0]==-1 and sETuple[0]==sBTuple[1] and sETuple[1]==(sBTuple[1][0]-1,sBTuple[1][1]):
        g.add_edge(sB,sE)
        #print("ajout4",sB,sE)
    elif sBTuple[0][0]==sBTuple[1][0] and sBTuple[1][1]-sBTuple[0][1]==1 and sETuple[0]==sBTuple[1] and sETuple[1]==(sBTuple[1][0],sBTuple[1][1]+1):
        g.add_edge(sB,sE)
        #print("ajout5",sB,sE)
    elif sBTuple[0][0]==sBTuple[1][0] and sBTuple[1][1]-sBTuple[0][1]==-1 and sETuple[0]==sBTuple[1] and sETuple[1]==(sBTuple[1][0],sBTuple[1][1]-1):
        g.add_edge(sB,sE)


def ajout(g,sommet,dicoinv):
    for s in g.nodes():
        if s!=sommet :
            ajout_arcs(g,sommet,s,dicoinv)
            ajout_arcs(g,s,sommet,dicoinv)
    
def recherche_chemin(graphe,positionInitiale:str,positionsfinales:set)->(bool,list):
    
    chemin=[]
    existe=False
    for s in positionsfinales :
        #print("s",s)
        #print(positionInitiale)
        try : 
            chemin =nx.astar_path(graphe,positionInitiale,s)
            existe=True
        except :
            pass
    return existe,chemin

def chemin(xmax,ymax):
   
    dico={ ((xf,yf),(xc,yc)):"("+str(xf)+","+str(yf)+"/"+str(xc)+","+str(yc)+")" for xf in range(1,xmax+1) for yf in range(1,ymax+1) for xc in range(1,xmax+1) for yc in range(1,ymax+1) if (xc,yc)!=(xf,yf)}
    dicoinv={"("+str(xf)+","+str(yf)+"/"+str(xc)+","+str(yc)+")":((xf,yf),(xc,yc)) for xf in range(1,xmax+1) for yf in range(1,ymax+1) for xc in range(1,xmax+1) for yc in range(1,ymax+1) if (xc,yc)!=(xf,yf)}
    
    positionInitiale=dico[((1,1),(1,2))]
    positionC=(1,ymax)
    
    positionsf={((positionC[0]-1,positionC[1]),positionC), ((positionC[0]+1,positionC[1]),positionC),((positionC[0],positionC[1]-1),positionC),((positionC[0],positionC[1]+1),positionC)}
    positionsfinales={dico[p] for p in positionsf if p in dico}
    g=nx.DiGraph()
    g.add_node(positionInitiale)
    

    for s in positionsfinales :
        g.add_node(s)
        ajout(g,s,dicoinv)
    
    sommets=[ value for keys, value in dico.items() if keys[0]!=keys[1] and value != positionInitiale and value not in positionsfinales]
    existe=False
    while not existe and len(sommets)>0:
        existe,chemin = recherche_chemin(g,positionInitiale,positionsfinales)
        if existe :
            return(chemin)
        else :
            s=sommets[0]
            del sommets[0]
            g.add_node(s)
            ajout(g,s,dicoinv)
            
    
 
        
def tempsChemin(xmax,ymax):
    t1=time.process_time()
    chemin(xmax,ymax)
    return time.process_time()-t1

abscisse=[]
ordonnee=[]

for t in range(2,12):

    xmax,ymax=t,t
    print("taile",t,"x",t)
    abscisse.append(t)
    ordonnee.append(tempsChemin(xmax,ymax))
plt.plot(abscisse,ordonnee)
print(abscisse,ordonnee)