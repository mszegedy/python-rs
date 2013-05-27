from math import sqrt,floor,atan

class vec: # a class for 2D vectors
    def __init__(self,i,j):
        self.x = i
        self.y = j
    def __repr__(self):
        return 'vec('+str(self.x)+','+str(self.y)+')'
    def __eq__(self,v):
        return (self.x == v.x) and (self.y == v.y)
    def __pos__(self):
        return self
    def __neg__(self):
        return vec(-self.x,-self.y)
    def __abs__(self):
        return sqrt(self.x**2+self.y**2)
    def __add__(self,v):
        return vec(self.x+v.x,self.y+v.y)
    def __sub__(self,v):
        return vec(self.x-v.x,self.y-v.y)
    def __mul__(self,v):
        if isinstance(v,vec):
            return self.x*v.x+self.y*v.y
        elif isinstance(v,int) or isinstance(v,float):
            return vec(v*self.x,v*self.y)
    def __rmul__(self,v):
        return self*v
    def __div__(self,r):
        return vec(self.x/r,self.y/r)
    def __pow__(self,r):
        return self.x**r+self.y**r
    def __int__(self):
        return int(abs(self))
    def __float__(self):
        return abs(self)
    def __str__(self):
        return '('+str(self.x)+','+str(self.y)+')'
    def __reversed__(self):
        return vec(self.y,self.x)
    def polar(self):
        return vec(abs(self),atan(self.y/self.x))
