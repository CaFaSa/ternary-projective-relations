import itertools
from collections import defaultdict


def inv(r):
    if r in L1:
        return L2[L1.index(r)]
    if r in L2:
        return L1[L2.index(r)]


def Constraints(rel1, rel2):
    comp = set()
    for r1 in rel1:
        for r2 in rel2:
            comp = comp.union(T[r1][r2])
    return comp


def INV(R):
    invR = set()
    for r in R:
        invR.add(inv(r))
    return invR


def Constraints2(rel1, rel2):
    t= CONV(rel2)
    q= ROT(t)
    p= CONV(rel1)
    return Constraints(p,q)


class ConstraintNetwork:
    def __init__(self, triplets={}):
        self.triplets = triplets

    def converse(self, rel):
        return

    def setrel(self, R1, R2, R3, rel):

        permutations = itertools.permutations(R1,R2,R3)
        for triplet in permutations:
            if triplet in self.triplets
                self.triplets[]

        if (R1, R2, R3) in self.triplets:
            self.triplets[R1, R2, R3] = rel
        elif (R2, R1) in self.triplets:
            self.triplets[R2, R1] = INV(rel)
        else: #non c'è
            self.triplets[R1, R2, R3] = rel

    def getrel(self, R1, R2, R3): #struttura analoga a setrel

        permutations = itertools.permutations(R1, R2, R3)
        if (R1, R2, R3) in self.triplets:
            return self.triplets[R1, R2, R3]
        elif (R2, R1) in self.triplets:
            return INV(self.triplets[R2, R1])
        else:
            return U #dd U dc


    def nodes(self):
        keys = self.triplets.keys()
        nodes = set()
        for (a, b, c) in keys:
            nodes.add(a)
            nodes.add(b)
            nodes.add(c)
        return nodes

    def adjtrip(self, R1, R2, R3):

        pass

    def addrel(self, R1, R2, R3, rel):
        C = self
        queue = []
        queue.append((R1, R2, R3))
        inters = C.getrel(R1, R2, R3).intersection(rel)
        C.setrel(R1, R2, R3, inters)
        while queue != []:
            # adjtrip deve considerare le adiacenze con 1-3 1-2 2-3
            (R1, R2, R3) = queue.pop(0)
            adjtrip = C.adjtrip(R1, R2, R3)

            for triplet in adjtrip:

                # per ogni triplet devo sapere le posizioni delle 2 regioni in comune (es 1,2   2,3   1,3)
                # oppure quello che è nuovo (Rnew ?)


                t1=(triplet[0], R2, R3)
                t2=(triplet[0], triplet[1], R3)
                #la newrel1 è incompleta perchè dobbiamo applicare i constraint iniziando da quella non in comune (Rnew)
                # non si deve passare triplet a getrel ma bisogna individuare la permutazione. Rivedere i parametri
                newrel1 = Constraints(C.getrel(triplet), C.getrel(R1, R2, R3))
                newrel2 = Constraints2(C.getrel(triplet), C.getrel(R1, R2, R3))


                oldrel = C.getrel(t1)
                oldrel2 = C.getrel(t2)
                inters = oldrel.intersection(newrel1)
                inters2 = oldrel2.intersection(newrel2)
            if inters != oldrel:
                C.setrel(t1, inters)
                queue.append(t1)

            if inters2 != oldrel2:
                C.setrel(t2, inters2)
                queue.append(t2)




    def __str__(self):
        s = ''
        for arc in self.triplets:
            s = s + str(arc) + ': ' + str(C.triplets[arc]) + '\n'
        return s






C = ConstraintNetwork()
C.addrel('s', 'l', {'o', 'm'})
C.addrel('s', 'r', {'<', 'm', 'mi', '>'})
C.addrel('l', 'r', {'o', 's', 'd'})
C.addrel('l', 't', {'di', 'mi', 'f'})
C.addrel('s', 'u', {'oi', 'd', 'f'})
C.addrel('u', 't', {'<'})
C.addrel('r', 't', {'>', 'di', 'm'})
print(C)

# further work: find a topological interpretation with intervals

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
