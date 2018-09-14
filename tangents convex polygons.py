# -*- coding: utf-8 -*-
"""
@author: cleme
"""

from Model.shapes import *
from intersection import *

def starting_points(p1,p2):
    dmin=p1[0].distance(p2[0])
    a=p1[0]
    for P in p1:
        d=P.distance(p2[0])
        if d<dmin:
            dmin=d
            a=P
    dmin=p2[0].distance(p1[0])
    b=p2[0]
    for P in p2:
        d=P.distance(p1[0])
        if d<dmin:
            dmin=d
            b=P
    return (a,b) 
 
def tangentpoint(P,p,i):
    return (sideplr(P,p[i-1],p[i])<=0 and \
    sideplr(P,p[i],p[i+1])>0) or \
    (sideplr(P,p[i-1],p[i])>0 and \
    sideplr(P,p[i],p[i+1])<=0) 

def first_int_tangent(p1,a,p2,b):
    i=p1.index(a)
    j=p2.index(b)
    while not(tangentpoint(p2[j],p1,i) and \
         tangentpoint(p1[i],p2,j)):
        while not(tangentpoint(p2[j],p1,i)):
            i=i-1
        while not(tangentpoint(p1[i],p2,j)):
            j=j-1
    return Polyline([p1[i],p2[j]])

def second_int_tangent(p1,a,p2,b):
    i=p1.index(a)
    j=p2.index(b)
    while not(tangentpoint(p2[j],p1,i) and \
         tangentpoint(p1[i],p2,j)):
        while not(tangentpoint(p2[j],p1,i)):
            i=i+1
        while not(tangentpoint(p1[i],p2,j)):
            j=j+1
    return Polyline([p1[i],p2[j]])


A=Vertex(-3.1,2.1)
B=Vertex(-1.6,1)
C=Vertex(0,1.7)
D=Vertex(0.3,3)
E=Vertex(0,4)
F=Vertex(-0.9,4.9)
G=Vertex(-2,5)
H=Vertex(-3.3,4.8)
I=Vertex(-3.6,4)
J=Vertex(-3.7,3.2)

K=Vertex(1,3.6)
L=Vertex(1.1,2.8)
M=Vertex(1.6,1.9)
N=Vertex(2.1,1.8)
O=Vertex(3.1,2.9)
P=Vertex(2.8,3.7)
Q=Vertex(2,4.8)
R=Vertex(1.4,4.6)


p1=Polygon([I,J,A,B,C,D,E,F,G,H],'black','orange')
p1.draw()

p2=Polygon([K,L,M,N,O,P,Q,R],'black','orange')
p2.draw()

(a,b)=starting_points(p1,p2)
a.draw('red')
b.draw('blue')

tangent1=first_int_tangent(p1,a,p2,b)
tangent1.draw()

tangent2=second_int_tangent(p1,a,p2,b)
tangent2.draw()

print()
print((269, 126))

plt.show()
