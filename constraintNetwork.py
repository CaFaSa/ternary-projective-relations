#from rcc8_table import *
from rcc8_table import *



#viene implementata la tabella di slide 13 di "12_GIS - qualitative spatial reasoning - part II"
#OperatoriDiretti=['<','d','o','m','s','f','=']
#OperatoriInversi=['>','di','oi','mi','si','fi','=']


def inv(r):
    if r in OperatoriDiretti:
        return OperatoriInversi[OperatoriDiretti.index(r)]
    if r in OperatoriInversi:
        return OperatoriDiretti[OperatoriInversi.index(r)]

    
def Constraints(R1,R2):
    comp=set()
    print(R1)
    print(R2)
    for r1 in R1:
        for r2 in R2:
            comp=comp.union(T[r1][r2])
    return comp


def INV(R):
    invR=set()
    for r in R:
        invR.add(inv(r))
    return invR


class ConstraintNetwork:
    #arcs e' dizionario
    def __init__(self,arcs={}):
        self.arcs=arcs


    def setrel(self,a,b,R):
        if (a,b) in self.arcs:
            self.arcs[a,b]=R
        elif (b,a) in self.arcs:
            self.arcs[b,a]=INV(R)
        else:
            self.arcs[a,b]=R
    
    
    def getrel(self,a,b):
        if (a,b) in self.arcs:
            return self.arcs[a,b]
        elif (b,a) in self.arcs:
            return INV(self.arcs[b,a])
        else:
            return U


    def nodes(self):
        keys=self.arcs.keys()
        nodes=set()
        for (a,b) in keys:
            nodes.add(a)
            nodes.add(b)
        return nodes
    

    def addrel(self,i,j,R):     
        queue=[]
        queue.append((i,j))
        inters=self.getrel(i,j).intersection(R)
        self.setrel(i,j,inters)
        while queue!=[]:
            (i,j)=queue.pop(0)
            nodes=self.nodes()
            nodes.discard(i)
            nodes.discard(j)
            for k in nodes:    
                newrel=Constraints(self.getrel(k,i),self.getrel(i,j))
                oldrel=self.getrel(k,j)
                inters=oldrel.intersection(newrel)
                if inters!=oldrel:
                    self.setrel(k,j,inters)
                    queue.append((k,j))
            for k in nodes:    
                newrel=Constraints(self.getrel(i,j),self.getrel(j,k))
                oldrel=self.getrel(i,k)
                inters=oldrel.intersection(newrel)
                if inters!=oldrel:
                    self.setrel(i,k,inters)
                    queue.append((i,k))
        

    def __str__(self):
        s=''
        for arc in self.arcs:
            s=s+str(arc)+': '+str(C.arcs[arc])+'\n'
        return s


C=ConstraintNetwork()
C.addrel('Czech','EU','NTPP')
C.addrel('Russia','Greece','DC')
C.addrel('Russia','EU','EC')
C.addrel('Greece','EU','TPP')
print(C.arcs)





'''
C.setrel('s','l',{'o','m'})
C.setrel('s','r',{'<','m','mi','>'})
R=Constraints(C.getrel('l','s'),C.getrel('s','r'))
C.setrel('l','r',R)
newarc={'o','s','d'}
inters=C.getrel('l','r').intersection(newarc)
C.setrel('l','r',inters)
newarc=Constraints(C.getrel('s','l'),C.getrel('l','r'))
inters=C.getrel('s','r').intersection(newarc)
C.setrel('s','r',inters)
print(C)
'''
