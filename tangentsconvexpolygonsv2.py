# -*- coding: utf-8 -*-
"""
@author: cleme
"""

from shapes import *
from osgeo import ogr
#from intersection import *


def tangentpointsxdx(point,polygon,i):
    return sideplr(point,polygon[(i-1)%len(polygon)],polygon[i])<=0 and sideplr(point,polygon[i],polygon[(i+1)%len(polygon)])>0

def tangentpointdxsx(point,polygon,i):
    return sideplr(point,polygon[(i-1)%len(polygon)],polygon[i])>0 and sideplr(point,polygon[i],polygon[(i+1)%len(polygon)])<=0


# p1, p2 poligoni
def first_int_tangent(polygon1,a,polygon2,b):
    tangent= ogr.Geometry(type=ogr.wkbLineString)

    i=polygon1.index(a)
    j=polygon2.index(b)
    length1=len(polygon1)
    length2=len(polygon2)
    while not(tangentpointsxdx(polygon2[j],polygon1,i) and tangentpointsxdx(polygon1[i],polygon2,j)):
        while not(tangentpointsxdx(polygon2[j],polygon1,i)):
            i=(i-1)%length1
        while not(tangentpointsxdx(polygon1[i],polygon2,j)):
            j=(j-1)%length2

    tangent.AddPoint_2D(polygon1[i][0],polygon1[i][1])
    tangent.AddPoint_2D(polygon2[j][0],polygon2[j][1])

    return tangent


def second_int_tangent(polygon1,a,polygon2,b):
    tangent= ogr.Geometry(type=ogr.wkbLineString)

    i=polygon1.index(a)
    length1=len(polygon1)
    length2=len(polygon2)
    j=polygon2.index(b)
    while not(tangentpointdxsx(polygon2[j],polygon1,i) and tangentpointdxsx(polygon1[i],polygon2,j)):
        while not(tangentpointdxsx(polygon2[j],polygon1,i)):
            i=(i+1)%length1
        while not(tangentpointdxsx(polygon1[i],polygon2,j)):
            j=(j+1)%length2

    tangent.AddPoint_2D(polygon1[i][0],polygon1[i][1])
    tangent.AddPoint_2D(polygon2[j][0],polygon2[j][1])

    return tangent


def sideplr(point, polygon1_point, polygon2_point):
    """
    Calculates the side of point p to the vector p1p2.
    Input
      p: the point
      p1, p2: the start and end points of the line
    Output
      -1: p is on the left side of p1p2
       0: p is on the line of p1p2
       1: p is on the right side of p1p2
    """
    return (point[0]-polygon1_point[0])*(polygon2_point[1]-polygon1_point[1])-(polygon2_point[0]-polygon1_point[0])*(point[1]-polygon1_point[1])


def main():
    A=Vertex(-3.1,5.1)
    B=Vertex(-1.6,4)
    C=Vertex(0,4.7)
    D=Vertex(0.3,6)
    E=Vertex(0,7)
    F=Vertex(-0.9,7.9)
    G=Vertex(-2,8)
    H=Vertex(-3.3,7.8)
    I=Vertex(-3.6,7)
    J=Vertex(-3.7,6.2)

    K=Vertex(-7,11.6)
    L=Vertex(-3,15.8)
    M=Vertex(1.6,17.9)
    O=Vertex(3.1,16.9)
    Q=Vertex(2,10.18)

    p1=Polygon([A,B,C,D,E,F,G,H,I,J],'black','orange')
    p1.draw()
    print(p1)

    p2=Polygon([K,L,M,O,Q],'black','orange')
    p2.draw()


    tangent1=first_int_tangent(p1,p1[0],p2,p2[0])
    tangent1.draw()

    tangent2=second_int_tangent(p1,p1[0],p2,p2[0])
    tangent2.draw()
    plt.show()


if __name__ == "__main__":
    main()
