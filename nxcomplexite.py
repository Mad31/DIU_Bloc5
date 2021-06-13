#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 11 21:53:08 2021

@author: a.rb
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun  8 09:29:54 2021

@author: a.rb
"""
import networkx as nx
from math import inf
import time as time
from matplotlib import pyplot


def chemin(xmax,ymax):
    positionInitiale=((1,1),(xmax//2+1,ymax//2+1))
    positionC=(xmax,ymax)
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

def tempsChemin(xmax,ymax):
    t1=time.process_time()
    chemin(xmax,ymax)
    return time.process_time()-t1
abscisse=[]
ordonnee=[]

for t in range(2,15):

    xmax,ymax=t,t
    print("taile",t,"x",t)
    abscisse.append(t)
    ordonnee.append(tempsChemin(xmax,ymax))
pyplot.plot(abscisse,ordonnee)
print(abscisse,ordonnee)
    