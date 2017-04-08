import math
import random
import lib.vectors.quaternion

tolerance = 0.0000001

class Vec3:

    def __init__(self,*args):
        if isinstance(args[0],Vec3):
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
        else:
            self.x = args[0]
            self.y = args[1]
            self.z = args[2]

    def cloneFrom(self,v):
        self.x = v.x
        self.y = v.y
        self.z = v.z

    def cloneInto(self,v):
        v.x = self.x
        v.y = self.y
        v.z = self.z

    def clone(self):
        return Vec3(self)

    def __str__(self):
        return "(" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ")"

    def __add__(self,q):
        x = self.x + q.x
        y = self.y + q.y
        z = self.z + q.z
        return Vec3(x,y,z)

    def __radd__(self,q):
        x = self.x + q.x
        y = self.y + q.y
        z = self.z + q.z
        return Vec3(x,y,z)
        
    
    def __sub__(self,q):
        x = self.x - q.x
        y = self.y - q.y
        z = self.z - q.z
        return Vec3(x,y,z)

    def __rsub__(self,q):
        x = q.x - self.x
        y = q.y - self.y
        z = q.z - self.z
        return Vec3(x,y,z)

    def __mul__(self,q):
        x = self.x * q
        y = self.y * q
        z = self.z * q
        return Vec3(x,y,z)

    def __rmul__(self,q):
        x = self.x * q
        y = self.y * q
        z = self.z * q
        return Vec3(x,y,z)

    def __truediv__(self,q):
        x = self.x / q
        y = self.y / q
        z = self.z / q
        return Vec3(x,y,z)

    def __neg__(self):
        return Vec3(-self.x,-self.y,-self.z)

    def __pos__(self):
        return Vec3(self)

    def __abs__(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def __eq__(self,q):
        if self.x != q.x:
            return False
        if self.y != q.y:
            return False
        if self.z != q.z:
            return False
        return True
    
    def __ne__(self,q):
        if self.x != q.x:
            return True
        if self.y != q.y:
            return True
        if self.z != q.z:
            return True
        return False

    def __copy__(self):
        return Vec3(self)
    
    def lenSqr(self):
        return self.x*self.x + self.y*self.y + self.z*self.z

    def len(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def dist(self,q):
        x = self.x - q.x
        y = self.y - q.y
        z = self.z - q.z
        return math.sqrt(x*x + y*y + z*z)
    
    def distSqr(self,q):
        x = self.x - q.x
        y = self.y - q.y
        z = self.z - q.z
        return x*x + y*y + z*z

    def dot(self,q):
        return self.x * q.x + self.y * q.y + self.z * q.z

    def cross(self,q):
        return Vec3(self.y * q.z - self.z * q.y, self.z * q.x - self.x * q.z, self.x * q.y - self.y * q.x)

    def __pow__(self,n):
        if isinstance(n,lib.vectors.quaternion.Quaternion):
            return self.applyQuaternion(n)

    
    def normalise(self):
        l = self.len()
        if l != 0:
            return Vec3(self.x/l,self.y/l,self.z/l)
        else:
            return Vec3(1,0,0)

    def toQuaternion(self):
        return lib.vectors.quaternion.Quaternion(0,self.x,self.y,self.z)

    def applyQuaternion(self,q):
        return q.__mul__(self.toQuaternion()).__mul__(q.conjugate()).vector()

    def rotateTo(self,v):
        if v.cross(self).len() < tolerance:
            if v.dot(self) >= -tolerance:
                return lib.vectors.quaternion.Quaternion(1,0,0,0)
            u = self.normalise()
            a,b,c = math.fabs(u.x), math.fabs(u.y), math.fabs(u.z)
            if a < b and a < c:
                v = Vec3(0,-u.z,u.y)
            elif b < c:
                v = Vec3(u.z,0,-u.x)
            else:
                v = Vec3(u.y,-u.x,0)
        else:
            u = self.normalise()
            v = u + v.normalise()
        v = v.normalise()
        d = u.dot(v)
        u = u.cross(v)
        return lib.vectors.quaternion.Quaternion(d,u.x,u.y,u.z)

def RandomUnitVec3():
    th = 2*math.pi*random.random()
    z = 2*random.random() - 1
    r = math.sqrt(1 - z*z)
    return Vec3(r*math.cos(th),r*math.sin(th),z)

def RandomVec3(*args):
    if len(args) == 1:
        radius = args[0]
    else:
        radius = 1
    th = 2*math.pi*random.random()
    z = 2*random.random() - 1
    r = math.sqrt(1 - z*z)
    radius *= math.sqrt(random.random())
    return Vec3(radius*r*math.cos(th),radius*r*math.sin(th),radius*z)

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
