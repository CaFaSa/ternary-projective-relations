import itertools
from collections import defaultdict
from Model.Relations import *
from Model.Relations import _Operations

'''
def Constraints(re1, re2):
    comp = set()
    for r1 in re1:
        for r2 in re2:
            comp = comp.union(_Operations.composition(r1,r2))
    return comp

def conv(R):
    convR = set()
    for r in R:
        convR.add(r.converse())
    return convR

def rot(R):
    rotR = set()
    for r in R:
        rotR.add(r.rotate())
    return rotR
'''
class ConstraintNetwork:
    def __init__(self, triplets={}):
        self.triplets = triplets

    def setrel(self, R1, R2, R3, rel):
        #if the triplet is already in the dictionary in any of its permutations,
        #it removes the entry and stores the new relation
        permutations = tuple(itertools.permutations((R1,R2,R3)))
        for triplet in permutations:
            if triplet in self.triplets.keys():
                del self.triplets[triplet]
        self.triplets[R1, R2, R3] = rel

    def OperatorTable(self,i):
        array_op=[lambda x: x, lambda x: ProjectiveRelation.converse(x), \
                  lambda x: ProjectiveRelation.rotate(ProjectiveRelation.converse(x)), \
                  lambda x: ProjectiveRelation.rotate(x), \
                  lambda x: ProjectiveRelation.converse(ProjectiveRelation.rotate(ProjectiveRelation.converse(x))), \
                  lambda x: ProjectiveRelation.converse(ProjectiveRelation.rotate(x))]
        return array_op[i]

    def getrel(self, R1, R2, R3):
        permutations = tuple(itertools.permutations((R1, R2, R3)))
        for i in range(len(permutations)):
            triplet=permutations[i]
            if triplet in self.triplets.keys():
                r=self.triplets[triplet] #it finds the relation stored in the dictionary
                OP=self.OperatorTable(i)
                r1=OP(r) #based on the permutation, we need to apply the necessary operators to find the relation that holds for R1,R2,R3
                return r1
        return U #dd U dc , in this case there are no stored permutations

    def nodes(self):
        keys = self.triplets.keys()
        nodes = set()
        for (a, b, c) in keys:
            nodes.add(a)
            nodes.add(b)
            nodes.add(c)
        return nodes

    def adjtrip(self, R1, R2, R3):
        '''
        It finds triplets of regions in the current network having two regions in common with triplet (R1,R2,R3)
        It only works with tuples in the given order, that is, it doesn't check for permutations
        It returns a set of tuples
        '''
        keys = self.triplets.keys()
        adjtrip = set()
        subset1 = set()
        subset2 = set()
        subset3 = set()
        set1 = set()
        set1.add((R1, R2, R3))
        subset1.update([R1, R2])
        subset2.update([R1, R3])
        subset3.update([R2, R3])
        for (a, b, c) in keys:
            set0=set()
            set0.update([a, b, c])
            if subset1.issubset(set0) or subset2.issubset(set0) or subset3.issubset(set0):
                adjtrip.add((a, b, c))
        adjtrip = adjtrip - set1 #this set difference removes the triplet (R1,R2,R3) from the result
        return adjtrip

    def regions_in_common(self,regions, triplet):
    # the two given triplets must have two elements in common
    # the function returns a tuple (RA,RB,RC,RD) where RA is the region not in common in (R1,R2,R3),
    # RB and RC are the regions in common,
    # and RD is the region not in common in <triplet>
        (RA, RB, RC, RD) = (None, None, None, None)
        (R1, R2, R3)=regions
        abcset=set()
        abcset.update(triplet)
        if R1 not in triplet:
            (RA,RB,RC)=(R1,R2,R3)
            abcset.remove(R2)
            abcset.remove(R3)
        if R2 not in triplet:
            (RA, RB, RC) = (R2, R1, R3)
            abcset.remove(R1)
            abcset.remove(R3)
        if R3 not in triplet:
            (RA, RB, RC) = (R3, R1, R2)
            abcset.remove(R1)
            abcset.remove(R2)
        RD = abcset.pop()
        return (RA, RB, RC, RD)

    def addrel(self, R1, R2, R3, rel):
        C = self
        queue = []
        queue.append((R1, R2, R3))
        r = C.getrel(R1, R2, R3)
        inters=r.intersection(rel)
        C.setrel(R1, R2, R3, inters)
        while queue != []:
            # adjtrip finds triplets with two regions in common with (R1,R2,R3)
            (R1, R2, R3) = queue.pop(0)
            adjtrip = C.adjtrip(R1, R2, R3)
            for triplet in adjtrip:
                #(R1,R2,R3) is the triplet to be added to the network
                # <triplet> is one of the adjacent triplets to (R1,R2,R3)
                # we need to find the regions that are in common with function regions_in_common:
                # where RA is the region not in common in (R1,R2,R3), RB and RC are the regions in common,
                # and RD is the region not in common in <triplet>
                (RA,RB,RC,RD)=self.regions_in_common((R1,R2,R3),triplet)
                # the two new triplets to be added to the network are (RA,RC,RD) and (RA,RB,RD)
                t1=(RA, RC, RD)
                t2=(RA, RB, RD)
                # getrel must take into account permutations
                # compositions to be calculated are RA,RB,RC + RB,RC,RD = RA,RC,RD
                # and RA,RC,RB + RC,RB,RD = RA,RB,RD
                r1=C.getrel(RA, RB, RC)
                r2=C.getrel(RB, RC, RD)
                newr1 = r1.composition(r2)
                r3=C.getrel(RA, RC, RB)
                r4=C.getrel(RC, RB, RD)
                newr2 = r3.composition(r4)
                oldr1 = C.getrel(RA, RC, RD)
                oldr2 = C.getrel(RA, RB, RD)
                inters1 = oldr1.intersection(newr1)
                inters2 = oldr2.intersection(newr2)
                if inters1 != oldr1:
                    C.setrel(RA, RC, RD, inters1)
                    queue.append(t1)
                if inters2 != oldr2:
                    C.setrel(RA, RB, RD, inters2)
                    queue.append(t2)

    def __str__(self):
        s = ''
        for arc in self.triplets:
            s = s + str(arc) + ': ' + str(C.triplets[arc]) + '\n'
        return s

if __name__ == '__main__':
    C = ConstraintNetwork()

    print("start. Adding first relation to C...")
    C.addrel('A', 'B', 'C','bf')
    print("done. Now adding second relation to C...")
    C.addrel('B', 'C', 'D','af')
    print("done! Now trying to print out C")

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
