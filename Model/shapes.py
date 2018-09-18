"""
A class for points polylines and polygons
"""

from math import sqrt
import matplotlib.pyplot as plt

class Point():
    """A class for points in Cartesian coordinate systems."""
    def __init__(self, x=None, y=None, key=None):
        self.x, self.y = x, y
        self.key = key
    def __getitem__(self, i):
        if i==0: return self.x
        if i==1: return self.y
        return None
    def __len__(self):
        return 2
    def __eq__(self, other):
        if isinstance(other, Point):
            return self.x==other.x and self.y==other.y
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    def __lt__(self, other):
        if isinstance(other, Point):
            if self.x<other.x:
                return True
            elif self.x==other.x and self.y<other.y:
                return True
            return False
        return NotImplemented
    def __gt__(self, other):
        if isinstance(other, Point):
            if self.x>other.x:
                return True
            elif self.x==other.x and self.y>other.y:
                return True
            return False
        return NotImplemented
    def __ge__(self, other):
        if isinstance(other, Point):
            if self > other or self == other:
                return True
            else:
                return False
            return False
        return NotImplemented
    def __le__(self, other):
        if isinstance(other, Point):
            if self < other or self == other:
                return True
            else:
                return False
            return False
        return NotImplemented
    def __str__(self):
        """NAP: Not a point"""
        if self.x is None or self.y is None or not isinstance(self.x, (int, float)) or not isinstance(self.y, (int, float)):
            return 'NAP'
        if isinstance(self.x, (int)):
            fmtstr = '({0}, '
        else:
            fmtstr = '({0:.1f}, '
        if isinstance(self.y, (int)):
            fmtstr += '{1})'
        else:
            fmtstr += '{1:.1f})'
        return fmtstr.format(self.x, self.y)
    def __repr__(self):
        return self.__str__()
    def distance(self, other):
        return sqrt((self.x-other.x)**2 + (self.y-other.y)**2)
    def draw(self,color):
        plt.plot(self.x,self.y,color=color,marker='.')
    def above(self,other):
        return self.y>other.y

def sideplr(p, p1, p2):
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
    return (p.x-p1.x)*(p2.y-p1.y)-(p2.x-p1.x)*(p.y-p1.y)

## Two statuses of the left endpoint
ENDPOINT = 0   ## original left endpoint
INTERIOR = 1   ## interior in the segment

class Segment:
    """
    A class for line segments.
    """
    def __init__(self, e, p0, p1, c=None):
        """
        Constructor of Segment class.
        Input
          e: segment ID, an integer
          p0, p1: endpoints of segment, Point objects
        """
        if p0>=p1:
            p0,p1 = p1,p0           # p0 is always left
        self.edge = e               # ID, in all edges
        self.lp = p0                # left point
        self.lp0 = p0               # original left point  #*@\label{lineseg:lp0}
        self.rp = p1                # right point
        self.status = ENDPOINT      # status of segment
        self.c = c                  # c: feature ID
    def __eq__(self, other):
        if isinstance(other, Segment):
            return (self.lp==other.lp and self.rp==other.rp)\
                or (self.lp==other.rp and self.rp==other.lp)
        return NotImplemented
    def __ne__(self, other):
        result = self.__eq__(other)
        if result is NotImplemented:
            return result
        return not result
    def __lt__(self, other): 
        if isinstance(other, Segment):
            if self.lp and other.lp:
                lr = sideplr(self.lp, other.lp, other.rp)
                if lr == 0:
                    lrr = sideplr(self.rp, other.lp, other.rp)
                    if other.lp.x < other.rp.x:
                        return lrr > 0
                    else:
                        return lrr < 0
                else:
                    if other.lp.x > other.rp.x:
                        return lr < 0
                    else:
                        return lr > 0
        return NotImplemented
    def __gt__(self, other):
        result = self.__lt__(other)
        if result is NotImplemented:
            return result
        return not result
    def __repr__(self):
        return "{0}".format(self.edge)
    def contains(self, p):
        """
        Returns none zero if segment has p as an endpoint
        """
        if self.lp == p:
            return -1
        elif self.rp == p:
            return 1
        else:
            return 0
    def lowerpoint(self):
        if self.lp.y<self.rp.y:
            return self.lp
        else:
            return self.rp
    def upperpoint(self):
        if self.lp.y>self.rp.y:
            return self.lp
        else:
            return self.rp
        

class Vertex(Point):
    def __init__(self,x,y,key=None,ear=None,downward_cusp=False,upward_cusp=False,first_edge=None,second_edge=None,inters_edge_l=None,inters_edge_r=None,side=None):
        Point.__init__(self,x,y,key)
        self.ear=ear
        self.downward_cusp=downward_cusp
        self.upward_cusp=upward_cusp
        self.first_edge=first_edge
        self.second_edge=second_edge
        self.inters_edge_l=inters_edge_l
        self.inters_edge_r=inters_edge_r
        self.side=side
        
class Shape():
    def __init__(self,points,id=None,t=None):
        self.points=points
        self.id=id
        self.type=t
    def __len__(self):
        return len(self.points)
    def __repr__(self):
        return str(self.points)
    def __iter__(self):
        return iter(self.points)
    def __delitem__(self,i):
        index=i%len(self)
        del self.points[index]
    def __getitem__(self,i):
        index=i%len(self)
        return self.points[index]
    def append(self,point):
        return self.points.append(point)
    def pop(self):
        self.points.pop()
    def index(self,point):
        return self.points.index(point)
    
    
class Polyline(Shape):
    def __init__(self,points,color='grey',id=None,name=None):
        Shape.__init__(self,points,id,"polyline")
        self.name=name
        self.color=color
    def draw(self):
        line_xcoord=[point.x for point in self.points]
        line_ycoord=[point.y for point in self.points]
        plt.plot(line_xcoord,line_ycoord,color=self.color)
        
class Polygon(Shape):
    def __init__(self,points,edgecolor='grey',fillcolor='white',id=None,name=None):
        Shape.__init__(self,points,id,"polygon")
        self.name=name
        self.fillcolor=fillcolor
        self.edgecolor=edgecolor
        
    def area(self):
        numvert=len(self)
        A=0
        for i in range(numvert):
            ai=self[i].x*self[i+1].y-self[i+1].x*self[i].y
            A=A+ai
        A=A/2.0
        return A

    def centroid(self):
        numvert=len(self)
        A=0
        xmean=0
        ymean=0
        for i in range(numvert):
            ai=self[i].x*self[i+1].y-self[i+1].x*self[i].y
            A=A+ai
            xmean=xmean+(self[i].x+self[i+1].x)*ai
            ymean=ymean+(self[i].y+self[i+1].y)*ai                        
        C=Point(xmean/(3*A),ymean/(3*A))
        return C
    
    def edge_list(self):
        edge_list=[]
        n=len(self.points)
        for i in range(n-1):
            edge=Segment(i,self.points[i],self.points[i+1])
            edge_list=edge_list+[edge]
        edge=Segment(n-1,self.points[n-1],self.points[0])
        edge_list=edge_list+[edge]
        return edge_list
    
    def incident_edges(self,vertex):
        return [edge for edge in self.edge_list() if vertex==edge.rp or vertex==edge.lp]
        
    def draw(self):
        poly_xcoord=[point.x for point in self.points]
        poly_ycoord=[point.y for point in self.points]
        plt.fill(poly_xcoord,poly_ycoord,closed=True,fill=True,
                 facecolor=self.fillcolor,
                 edgecolor=self.edgecolor,alpha=0.5)
        
