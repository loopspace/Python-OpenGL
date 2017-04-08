import math

class Vec2:

    def __init__(self,*args):
        if isinstance(args[0],Vec2):
            self.x = args[0].x
            self.y = args[0].y
        else:
            self.x = args[0]
            self.y = args[1]

    def cloneFrom(self,v):
        self.x = v.x
        self.y = v.y

    def cloneInto(self,v):
        v.x = self.x
        v.y = self.y

    def clone(self):
        return Vec2(self)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ")"

    def __add__(self,q):
        x = self.x + q.x
        y = self.y + q.y
        return Vec2(x,y)

    def __radd__(self,q):
        x = self.x + q.x
        y = self.y + q.y
        return Vec2(x,y)
        
    
    def __sub__(self,q):
        x = self.x - q.x
        y = self.y - q.y
        return Vec2(x,y)

    def __rsub__(self,q):
        x = q.x - self.x
        y = q.y - self.y
        return Vec2(x,y)

    def __mul__(self,q):
        if isinstance(q,Vec2):
            x = self.x * q.x - self.y * q.y
            y = self.x * q.y + self.y * q.x
        else:
            x = self.x * q
            y = self.y * q
        return Vec2(x,y)

    def __rmul__(self,q):
        if isinstance(q,Vec2):
            x = self.x * q.x - self.y * q.y
            y = self.x * q.y + self.y * q.x
        else:
            x = self.x * q
            y = self.y * q
        return Vec2(x,y)

    def __truediv__(self,q):
        if isinstance(q,Vec2):
            l = q.lenSqr()
            x = (self.x * q.x + self.y * q.y)/l
            y = (self.y * q.x - self.x * q.y)/l
        else:
            x = self.x / q
            y = self.y / q
        return Vec2(x,y)

    def __rtruediv__(self,q):
        if isinstance(q,Vec2):
            l = self.lenSqr()
            x = (q.x * self.x + q.y * self.y)/l
            y = (q.y * self.x - q.x * self.y)/l
        else:
            l = self.lenSqr()
            x = q * self.x/l
            y = - q * self.y/l
        return Vec2(x,y)

    def __neg__(self):
        return Vec2(-self.x,-self.y)

    def __pos__(self):
        return Vec2(self)

    def __abs__(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def __invert__(self):
        return Vec2(self.x,-self.y)

    def conjugate(self):
        return Vec2(self.x,-self.y)

    def __eq__(self,q):
        if self.x != q.x:
            return False
        if self.y != q.y:
            return False
        return True
    
    def __ne__(self,q):
        if self.x != q.x:
            return True
        if self.y != q.y:
            return True
        return False

    def __copy__(self):
        return Vec2(self)
    
    def lenSqr(self):
        return self.x*self.x + self.y*self.y

    def len(self):
        return math.sqrt(self.x*self.x + self.y*self.y)

    def dist(self,q):
        x = self.x - q.x
        y = self.y - q.y
        return math.sqrt(x*x + y*y)
    
    def distSqr(self,q):
        x = self.x - q.x
        y = self.y - q.y
        return x*x + y*y

    def dot(self,q):
        return self.x * q.x + self.y * q.y

    def cross(self,q):
        return self.x * q.y - self.y * q.x
    
    def normalise(self):
        l = self.len()
        if l != 0:
            return Vec2(self.x/l,self.y/l)
        else:
            return Vec2(1,0)

    def rotate90(self):
        return Vec2(-self.y,self.x)
        
    def rotate(self,a):
        return Vec2(math.cos(a)*self.x - math.sin(a)*self.y,math.sin(a)*self.x + math.cos(a)*self.y)

# Tests
if __name__ == "__main__":
    q = Quaternion(1,-2,0,0)
    qq = Quaternion(q)
    i = Quaternion(0,1,0,0)
    j = Quaternion(0,0,1,0)
    k = Quaternion(0,0,0,1)
    u = Vec3(1,-2,3)
    v = Vec3(u)
    print(u)
    print(v)
    print(u + v)
    print(3 * u)
    print(v * 3)
    print(u != v)
    print(u.toQuaternion() * j)
    print(j * u.toQuaternion())
    print(u ** i)
    print(u ** j)
    print(u ** k)
    u = Vec3(0.8,0.6,0)
    v = Vec3(0,0.6,0.8)
    print(u)
    print(u ** k)
    print(v)
    w = u ** u.rotateTo(v)
    q = u.rotateTo(v)
    print(u.rotateTo(v))
    print(w)
    print(u.len())
    print(w.len())
    print(qRotation(math.pi/2,1,0,0))
    '''
    print(i * u.toQuaternion())
    print(u.applyQuaternion(i))
    print(u ** j)
    print(u ** k)
    print(v)
    print(q)
    print(qq)
    print(q + qq)
    print(q + 3)
    print(q * qq)
    print(q * qq / q)
    print(3 - q)
    print(i * j)
    print(j * k)
    print(k * i)
    print(3 * q)
    print(q * 3)
    print(1/i)
    print(q * ~q)
    print(q != qq)
    print(q ** 2 / q)
    '''
