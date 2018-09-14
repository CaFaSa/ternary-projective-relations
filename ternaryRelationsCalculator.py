import matplotlib.pyplot as plt
import subprocess
import numpy as np
import random
from osgeo import ogr
from sys import platform
from numpy.linalg import lstsq
from numpy import ones,vstack
from math import sqrt,tan,atan,floor,atan2,pi
import decimal
from tangentsconvexpolygonsv2 import first_int_tangent,second_int_tangent

class PlotUtilities:
    def __init__(self):
        pass

    def get_random_color(self,pastel_factor = 0.1):
        return [(x+pastel_factor)/(1.0+pastel_factor) for x in [random.uniform(0,1.0) for i in [1,2,3]]]

    def plot_rings(self,geom,color):
        ring=geom.GetGeometryRef(0)
        points = ring.GetPoints()
        ptsx = [p[0] for p in points]
        ptsy = [p[1] for p in points]
        args=(ptsx,ptsy)
        plt.fill(*args,closed=True,fill=True,
                    facecolor=color,
                    linewidth=0.1,
                    edgecolor='red',alpha=0.5)
        n=geom.GetGeometryCount()
        args=()
        for i in range(1,n):
            ring=geom.GetGeometryRef(i)
            points=ring.GetPoints()        
            ptsx=[p[0] for p in points]
            ptsy=[p[1] for p in points]
            args=args+(ptsx,ptsy)
        plt.fill(*args, closed=True, fill=True,
                facecolor='white',
                linewidth=0.1,
                edgecolor='red', alpha=0.5)


class ComputationalGeometryUtilities:
    def __init__(self):
        pass

    def buildSegment(self,pointOfIntersection,angularCoefficient,intercept,stepLength,orientation):
        line=ogr.Geometry(type=ogr.wkbLineString)
        newPointX=pointOfIntersection.GetPoints()[0][0]
        line.AddPoint_2D(newPointX,(newPointX*angularCoefficient)+intercept)
        newPointX=pointOfIntersection.GetPoints()[0][0]+stepLength*orientation
        line.AddPoint_2D(newPointX,(newPointX*angularCoefficient)+intercept)
        return line

    def createPolygon(self,pointsList):
        ring=ogr.Geometry(ogr.wkbLinearRing)
        for point in pointsList:
            if isinstance(point,tuple):
                ring.AddPoint_2D(point[0],point[1])
            else:
                ring.AddPoint_2D(point.GetX(),point.GetY())

        ring.AddPoint_2D(ring.GetPoints()[0][0],ring.GetPoints()[0][1])

        poly=ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)

        return poly


    def randomPolyGenerator(self,numberOfPoints,otherPolygon,totallyRandom=False):
        ring=ogr.Geometry(type=ogr.wkbLinearRing)
        if not totallyRandom:
            for i in range(0,numberOfPoints):
                if otherPolygon == None:
                    ring.AddPoint_2D(round(random.uniform(0,30),2),round(random.uniform(70,120),2))
                else:
                    ring.AddPoint_2D(round(random.uniform(60,90),2),round(random.uniform(70,120),2))
        else:
            for i in range(0,numberOfPoints):
                ring.AddPoint_2D(round(random.uniform(0,90),2),round(random.uniform(0,120),2))       
  
        ring.AddPoint_2D(ring.GetPoints()[0][0],ring.GetPoints()[0][1])
        poly=ogr.Geometry(type=ogr.wkbPolygon)
        poly.AddGeometry(ring)
        return poly


    def getPointCloudCentre(self,pointList):
        numberOfPoints=len(pointList)
        x=0
        y=0
        for point in pointList:
            x=x+point.GetX()
            y=y+point.GetY()
        return (x/numberOfPoints,y/numberOfPoints)


    def sortPointsClockwise(self,pointList):
        def algo(point):
            #return (atan2(point.GetX() - centre[0], point.GetY() - centre[1]) + 2 * pi) % (2*pi) funzionante
            return (atan2(point.GetX() - centre[0], point.GetY() - centre[1]) + 2 * pi)
        centre=self.getPointCloudCentre(pointList)
        pointList.sort(key=algo)
        return pointList


    def closePolygon(self,polygon):
        pointList=polygon.GetGeometryRef(0).GetPoints()
        if pointList[0] != pointList[len(pointList)-1]:
            pointList.append(pointList[0])
            newPolygon = self.createPolygon(pointList)
            return newPolygon
        else:
            return polygon

    def buildLongLine(self,pointOfIntersection,angularCoefficient,intercept,stepLength):
        if isinstance(pointOfIntersection,ogr.Geometry):
            pointOfIntersection=pointOfIntersection.GetPoints()[0]
        line=ogr.Geometry(type=ogr.wkbLineString)
        newPointX=pointOfIntersection[0]
        line.AddPoint_2D(newPointX,newPointX*angularCoefficient+intercept)
        newPointX=pointOfIntersection[0]+stepLength
        line.AddPoint_2D(newPointX,newPointX*angularCoefficient+intercept)
        newPointX=pointOfIntersection[0]
        line.AddPoint_2D(newPointX,newPointX*angularCoefficient+intercept)
        newPointX=pointOfIntersection[0]-stepLength
        line.AddPoint_2D(newPointX,newPointX*angularCoefficient+intercept)
        
        return line


    def linestringToPolygon(self,linestring):
        ring= ogr.Geometry(ogr.wkbLinearRing)
        for point in linestring.GetPoints():
            ring.AddPoint_2D(point[0],point[1])
        poly = ogr.Geometry(ogr.wkbPolygon)
        poly.AddGeometry(ring)
        return poly


    def lineEquation(self,puntoA,puntoB):
        if isinstance(puntoA, ogr.Geometry) and isinstance(puntoB, ogr.Geometry):

            points = [(puntoA.GetPoints()[0][0],puntoA.GetPoints()[0][1]),(puntoB.GetPoints()[0][0],puntoB.GetPoints()[0][1])]
        elif isinstance(puntoA, tuple) and isinstance(puntoB, tuple):
            points = [(puntoA[0],puntoA[1]),(puntoB[0],puntoB[1])]

        x_coords, y_coords = zip(*points)
        A = vstack([x_coords,ones(len(x_coords))]).T
        m, c = lstsq(A, y_coords)[0]
        return m,c 


    def getBisectors(self,tangentLinestring1,tangentLinestring2,centre):
        puntoA= ogr.Geometry(type=ogr.wkbPoint)
        puntoB= ogr.Geometry(type=ogr.wkbPoint)    
        puntoA.AddPoint_2D(tangentLinestring1.GetPoints()[0][0],tangentLinestring1.GetPoints()[0][1])
        puntoB.AddPoint_2D(tangentLinestring1.GetPoints()[1][0],tangentLinestring1.GetPoints()[1][1])   
        a, c= self.lineEquation(puntoA,puntoB)

        puntoC= ogr.Geometry(type=ogr.wkbPoint)
        puntoD= ogr.Geometry(type=ogr.wkbPoint)    
        puntoC.AddPoint_2D(tangentLinestring2.GetPoints()[0][0],tangentLinestring2.GetPoints()[0][1])
        puntoD.AddPoint_2D(tangentLinestring2.GetPoints()[1][0],tangentLinestring2.GetPoints()[1][1])   
        A, C= self.lineEquation(puntoC,puntoD)
        a=a*-1
        A=A*-1
        
        angularCoefficient1=(-1)*((a*A-1+sqrt(a**2+1)*sqrt(A**2+1))/(a+A))
        angularCoefficient2=((a+A)/(a*A-1+sqrt(a**2+1)*sqrt(A**2+1)))
        intercept1=angularCoefficient1*(-1)*centre.GetPoints()[0][0]+centre.GetPoints()[0][1]
        intercept2=angularCoefficient2*(-1)*centre.GetPoints()[0][0]+centre.GetPoints()[0][1]
        return self.buildLongLine(centre,angularCoefficient1,intercept1,puntoA.Distance(puntoB)*10),self.buildLongLine(centre,angularCoefficient2,intercept2,puntoA.Distance(puntoB)*10)


class ternaryRelationCalculator:
    boundary_min_XY=0
    boundary_max_XY=0
    boundaryPolygon=None
    boundaryLines=None
    CGU=ComputationalGeometryUtilities()
    PU=PlotUtilities()
    firstPolygon=None
    secondPolygon=None
    thirdPolygon=None
    firstTangent=None
    secondTangent=None
    tangentIntersectionPoint=None
    intersectionList=None
    areas=None
    twoPolygonsConvexHull=None
    polygonsAreIntersecting=False
    def __init__(self,boundary_minXY,boundary_maxXY,thirdPolygon,secondPolygon,firstPolygon=None):
        self.boundary_max_XY=boundary_maxXY
        self.boundary_min_XY=boundary_minXY
        self.boundaryLines,self.boundaryPolygon=self.externalBoundary()
        self.thirdPolygon=thirdPolygon.ConvexHull()
        self.secondPolygon=secondPolygon.ConvexHull()
        if not firstPolygon is None:
            self.firstPolygon=firstPolygon.ConvexHull()

        thirdPolygonPointList=self.thirdPolygon.GetGeometryRef(0).GetPoints()[:-1]
        secondPolygonPointList=self.secondPolygon.GetGeometryRef(0).GetPoints()[:-1]

        if secondPolygon.Intersects(thirdPolygon):
            self.polygonsAreIntersecting=True
            self.secondPolygon=secondPolygon.ConvexHull()
            self.thirdPolygon=thirdPolygon.ConvexHull()
            self.twoPolygonsConvexHull= self.secondPolygon.Union(self.thirdPolygon)
        else:
            self.firstTangent= first_int_tangent(thirdPolygonPointList, self.thirdPolygon.GetGeometryRef(0).GetPoint_2D(0), secondPolygonPointList,self.secondPolygon.GetGeometryRef(0).GetPoint_2D(0))
            self.secondTangent= second_int_tangent(thirdPolygonPointList, self.thirdPolygon.GetGeometryRef(0).GetPoint_2D(0), secondPolygonPointList,self.secondPolygon.GetGeometryRef(0).GetPoint_2D(0))
            self.tangentIntersectionPoint=self.firstTangent.Intersection(self.secondTangent)
            self.intersectionList=self.findIntersectionsWithBoundary(self.firstTangent)
            self.intersectionList.extend(self.findIntersectionsWithBoundary(self.secondTangent))
            self.twoPolygonsConvexHull= (thirdPolygon.Union(secondPolygon)).ConvexHull()
            self.areas=self.buildFourAreas(self.intersectionList,self.tangentIntersectionPoint)



    def tangentBoundaryIntersection(self,tangent,boundaryLine):
        m,c=self.CGU.lineEquation(tangent.GetPoints()[0],tangent.GetPoints()[1])
        tangent=self.CGU.buildLongLine(tangent.GetPoint_2D(0),m,c,5000)
        if tangent.Intersects(boundaryLine):
            return tangent.Intersection(boundaryLine)
        else:
            return None


    def findIntersectionsWithBoundary(self,line):
        intersections=[]
        for boundaryLine in self.boundaryLines:
            intersection = self.tangentBoundaryIntersection(line,boundaryLine)

            if not intersection is None:
                if (intersection.GetX()>=self.boundary_min_XY and intersection.GetY()>=self.boundary_min_XY and intersection.GetX()<=self.boundary_max_XY and intersection.GetY()<=self.boundary_max_XY):
                    intersections.append(intersection)
        return intersections


    def view(self):
        if not self.polygonsAreIntersecting:
            self.PU.plot_rings(self.CGU.linestringToPolygon(self.firstTangent),color=self.PU.get_random_color())
            self.PU.plot_rings(self.CGU.linestringToPolygon(self.secondTangent),color=self.PU.get_random_color())
            for intersection in self.intersectionList:
                plt.plot(intersection.GetX(),intersection.GetY(),color=self.PU.get_random_color(),marker='.')
            for area in self.areas:
                self.PU.plot_rings(area,color=self.PU.get_random_color())        

        self.PU.plot_rings(self.CGU.linestringToPolygon(self.boundaryLines[0]),color=self.PU.get_random_color())
        self.PU.plot_rings(self.CGU.linestringToPolygon(self.boundaryLines[1]),color=self.PU.get_random_color())
        self.PU.plot_rings(self.CGU.linestringToPolygon(self.boundaryLines[2]),color=self.PU.get_random_color())
        self.PU.plot_rings(self.CGU.linestringToPolygon(self.boundaryLines[3]),color=self.PU.get_random_color())
        self.PU.plot_rings(self.twoPolygonsConvexHull, color = 'black')
        #self.PU.plot_rings(self.secondPolygon, color = self.PU.get_random_color())
        #self.PU.plot_rings(self.thirdPolygon, color = self.PU.get_random_color())

        if not self.firstPolygon is None:
            self.PU.plot_rings(self.firstPolygon, color = self.PU.get_random_color())
        plt.show()


    def classify(self):
        relations=set()
        areaMeaning=["bf","ls","af","rs"]
        if self.polygonsAreIntersecting:
            if self.firstPolygon.Intersects(self.twoPolygonsConvexHull):
                if not self.twoPolygonsConvexHull.Contains(self.firstPolygon):
                    relations.add("in:ou")
                else:
                    relations.add("in")
            else:
                relations.add("ou")
        else:
            if self.firstPolygon.Intersects(self.twoPolygonsConvexHull):
                relations.add("bt")
            for area in self.areas:
                if self.firstPolygon.Intersects(area):
                    tempRelation=areaMeaning[self.areas.index(area)]
                    relations.add(tempRelation)

        fig = plt.figure()
        ax1 = fig.add_axes((0.1,0.1,0.8,0.8))
        ax1.set_title(relations)
        print(relations)
        return relations


    def buildFourAreas(self,tangentBoundaryIntersectionList,intersectionBetweenTangents):
        allPointsList=[]
        pointA=ogr.Geometry(type=ogr.wkbPoint)
        pointB=ogr.Geometry(type=ogr.wkbPoint)
        pointC=ogr.Geometry(type=ogr.wkbPoint)
        pointD=ogr.Geometry(type=ogr.wkbPoint)
        pointA.AddPoint_2D(self.boundary_min_XY,self.boundary_min_XY)
        pointB.AddPoint_2D(self.boundary_min_XY,self.boundary_max_XY)
        pointC.AddPoint_2D(self.boundary_max_XY,self.boundary_max_XY)
        pointD.AddPoint_2D(self.boundary_max_XY,self.boundary_min_XY)    
        allPointsList.append(pointA)
        allPointsList.append(pointB)
        allPointsList.append(pointC)
        allPointsList.append(pointD)
        allPointsList.extend(tangentBoundaryIntersectionList)
        allPointsList=self.CGU.sortPointsClockwise(allPointsList)
        polygonList=[]
        i=0
        while True:
            if allPointsList[i] in tangentBoundaryIntersectionList:
                newPolygonPointList=[]
                newPolygonPointList.append(allPointsList[i])
                k=(i+1)%len(allPointsList)
                while True:
                    if allPointsList[k] in tangentBoundaryIntersectionList:
                        newPolygonPointList.append(allPointsList[k])
                        newPolygonPointList.append(intersectionBetweenTangents)
                        polygonList.append(self.CGU.createPolygon(newPolygonPointList))
                        break
                    else:
                        newPolygonPointList.append(allPointsList[k])
                    k=(k+1)%len(allPointsList) 
            i=(i+1)%len(allPointsList)
            if(len(polygonList)==4):
                break


        areaList=[]
        for polygon in polygonList:
            areaList.append(polygon.Difference(self.twoPolygonsConvexHull))
        #return polygonList
        return areaList


    def externalBoundary(self):
        pointA= (self.boundary_min_XY,self.boundary_min_XY)
        pointB= (self.boundary_min_XY,self.boundary_max_XY)
        pointC= (self.boundary_max_XY,self.boundary_max_XY)
        pointD= (self.boundary_max_XY,self.boundary_min_XY)
        line1=ogr.Geometry(type=ogr.wkbLineString)
        line2=ogr.Geometry(type=ogr.wkbLineString)
        line3=ogr.Geometry(type=ogr.wkbLineString)
        line4=ogr.Geometry(type=ogr.wkbLineString)
        
        line1.AddPoint_2D(pointA[0],pointA[1])
        line1.AddPoint_2D(pointB[0],pointB[1])
        line2.AddPoint_2D(pointB[0],pointB[1])
        line2.AddPoint_2D(pointC[0],pointC[1])
        line3.AddPoint_2D(pointC[0],pointC[1])
        line3.AddPoint_2D(pointD[0],pointD[1])
        line4.AddPoint_2D(pointD[0],pointD[1])
        line4.AddPoint_2D(pointA[0],pointA[1])
        allPointsList=[]
        allPointsList.append(pointA)
        allPointsList.append(pointB)
        allPointsList.append(pointC)
        allPointsList.append(pointD)
        boundaryPolygon=self.CGU.createPolygon(allPointsList)
        lineList=[]
        lineList.append(line1)
        lineList.append(line2)
        lineList.append(line3)
        lineList.append(line4)
        return lineList,boundaryPolygon


def main():
    CGU=ComputationalGeometryUtilities()
    secondPolygon=CGU.randomPolyGenerator(12,None)
    thirdPolygon=CGU.randomPolyGenerator(15,secondPolygon)
    firstPolygon=CGU.randomPolyGenerator(4,None,totallyRandom=True)
    TRC=ternaryRelationCalculator(-100,200,thirdPolygon,secondPolygon,firstPolygon)
    TRC.classify()
    TRC.view()


if __name__=="__main__":
    main()



