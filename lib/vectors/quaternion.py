import math
import lib.vectors.vec3

class Quaternion:

    def __init__(self,*args):
        if isinstance(args[0],Quaternion):
            self.w = args[0].w
            self.x = args[0].x
            self.y = args[0].y
            self.z = args[0].z
        else:
            self.w = args[0]
            self.x = args[1]
            self.y = args[2]
            self.z = args[3]

    def cloneFrom(self,v):
        self.w = v.w
        self.x = v.x
        self.y = v.y
        self.z = v.z

    def cloneInto(self,v):
        v.w = self.w
        v.x = self.x
        v.y = self.y
        v.z = self.z

    def clone(self):
        return Quaternion(self)

    def __str__(self):
        s = ""
        signed = False
        if self.w != 0:
            s = str(self.w)
            signed = True
        for n in [[self.x,"i"],[self.y,"j"],[self.z,"k"]]:
            if n[0] != 0:
                if signed:
                    if n[0] > 0:
                        s += " + "
                        if n[0] != 1:
                            s += str(n[0])
                    else:
                        s += " - "
                        if n[0] != -1:
                            s += str(-n[0])
                else:
                    if n[0] != 1:
                        if n[0] == -1:
                            s += "-"
                        else:
                            s += str(n[0])
                s += n[1]
                signed = True
        if not signed:
            s = "0"
        return s

    def __add__(self,q):
        if isinstance(q,Quaternion):
            w = self.w + q.w
            x = self.x + q.x
            y = self.y + q.y
            z = self.z + q.z
        else:
            w = self.w + q
            x = self.x
            y = self.y
            z = self.z
        return Quaternion(w,x,y,z)

    def __radd__(self,q):
        if isinstance(q,Quaternion):
            w = self.w + q.w
            x = self.x + q.x
            y = self.y + q.y
            z = self.z + q.z
        else:
            w = self.w + q
            x = self.x
            y = self.y
            z = self.z
        return Quaternion(w,x,y,z)
        
    
    def __sub__(self,q):
        if isinstance(q,Quaternion):
            w = self.w - q.w
            x = self.x - q.x
            y = self.y - q.y
            z = self.z - q.z
        else:
            w = self.w - q
            x = self.x
            y = self.y
            z = self.z
        return Quaternion(w,x,y,z)

    def __rsub__(self,q):
        if isinstance(q,Quaternion):
            w = q.w - self.w
            x = q.x - self.x
            y = q.y - self.y
            z = q.z - self.z
        else:
            w = q - self.w
            x = -self.x
            y = -self.y
            z = -self.z
        return Quaternion(w,x,y,z)

    def __mul__(self,q):
        if isinstance(q,Quaternion):
            w = self.w * q.w - self.x * q.x - self.y * q.y - self.z * q.z
            x = self.w * q.x + self.x * q.w + self.y * q.z - self.z * q.y
            y = self.w * q.y - self.x * q.z + self.y * q.w + self.z * q.x
            z = self.w * q.z + self.x * q.y - self.y * q.x + self.z * q.w
        else:
            w = self.w * q
            x = self.x * q
            y = self.y * q
            z = self.z * q
        return Quaternion(w,x,y,z)

    def __rmul__(self,q):
        if isinstance(q,Quaternion):
            w = q.w * self.w - q.x * self.x - q.y * self.y - q.z * self.z
            x = q.w * self.x + q.x * self.w + q.y * self.z - q.z * self.y
            y = q.w * self.y - q.x * self.z + q.y * self.w + q.z * self.x
            z = q.w * self.z + q.x * self.y - q.y * self.x + q.z * self.w
        else:
            w = self.w * q
            x = self.x * q
            y = self.y * q
            z = self.z * q
        return Quaternion(w,x,y,z)

    def __truediv__(self,q):
        if isinstance(q,Quaternion):
            l = q.lenSqr()
            q = Quaternion(q.w/l,-q.x/l,-q.y/l,-q.z/l)
            w = self.w * q.w - self.x * q.x - self.y * q.y - self.z * q.z
            x = self.w * q.x + self.x * q.w + self.y * q.z - self.z * q.y
            y = self.w * q.y - self.x * q.z + self.y * q.w + self.z * q.x
            z = self.w * q.z + self.x * q.y - self.y * q.x + self.z * q.y
        else:
            w = self.w / q
            x = self.x / q
            y = self.y / q
            z = self.z / q
        return Quaternion(w,x,y,z)

    def __rtruediv__(self,q):
        l = self.lenSqr()
        qq = Quaternion(self.w/l,-self.x/l,-self.y/l,-self.z/l)
        if isinstance(q,Quaternion):
            w = q.w * qq.w - q.x * qq.x - q.y * qq.y - q.z * qq.z
            x = q.w * qq.x + q.x * qq.w + q.y * qq.z - q.z * qq.y
            y = q.w * qq.y - q.x * qq.z + q.y * qq.w + q.z * qq.x
            z = q.w * qq.z + q.x * qq.y - q.y * qq.x + q.z * qq.y
        else:
            w = qq.w
            x = qq.x
            y = qq.y
            z = qq.z
        return Quaternion(w,x,y,z)


    def __neg__(self):
        return Quaternion(-self.w,-self.x,-self.y,-self.z)

    def __pos__(self):
        return Quaternion(self)

    def __abs__(self):
        return math.sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)

    def __invert__(self):
        return Quaternion(self.w,-self.x,-self.y,-self.z)

    def conjugate(self):
        return Quaternion(self.w,-self.x,-self.y,-self.z)

    def __eq__(self,q):
        if self.w != q.w:
            return False
        if self.x != q.x:
            return False
        if self.y != q.y:
            return False
        if self.z != q.z:
            return False
        return True
    
    def __ne__(self,q):
        if self.w != q.w:
            return True
        if self.x != q.x:
            return True
        if self.y != q.y:
            return True
        if self.z != q.z:
            return True
        return False

    def __copy__(self):
        return Quaternion(self)
    
    def lenSqr(self):
        return self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z

    def len(self):
        return math.sqrt(self.w*self.w + self.x*self.x + self.y*self.y + self.z*self.z)

    def dist(self,q):
        w = self.w - q.w
        x = self.x - q.x
        y = self.y - q.y
        z = self.z - q.z
        return math.sqrt(w*w + x*x + y*y + z*z)
    
    def distSqr(self,q):
        w = self.w - q.w
        x = self.x - q.x
        y = self.y - q.y
        z = self.z - q.z
        return w*w + x*x + y*y + z*z

    def dot(self,q):
        return self.w * q.w + self.x * q.x + self.y * q.y + self.z * q.z

    def slen(self):
        q = self.normalise()
        q.w = q.w - 1
        return 2*math.asin(q.len()/2)

    def sdist(self,q):
        qq = self.normalise()
        q = q.normalise()
        return 2*math.asin(q.dist(qq)/2)

    def integerpower(self,n):
        if n == 0:
            return Quaternion(1,0,0,0)
        elif n > 0:
            return self.__mul__(self.integerpower(n-1))
        elif n < 0:
            l = self.lenSqr()
            q = Quaternion(self.w/l,-self.x/l,-self.y/l,-self.z/l)
            return q.integerpower(-n)

    def realpower(self,n):
        if isinstance(n,int):
            return self.integerpower(n)
        l = self.len()
        q = self.normalise()
        return (l ** n) * q.slerp(n)

    def __pow__(self,n):
        if isinstance(n,Quaternion):
            return n.__mul__(self).__div__(n)
        else:
            return self.realpower(n)
    
    def normalise(self):
        l = self.len()
        if l != 0:
            return Quaternion(self.w/l,self.x/l,self.y/l,self.z/l)
        else:
            return Quaternion(1,0,0,0)

    def lerp(self,*args):
        if len(args) == 1:
            q = Quaternion(1,0,0,0)
            qq = self
            t = args[0]
        else:
            q = self
            qq = args[0]
            t = args[1]
        if (q + qq).len() == 0:
            q = (1 - 2*t) * q + (1 - math.fabs(2*t - 1)) * Quaternion(q.x,-q.w,q.z,-q.y)
        else:
            q = (1 - t)*q + t*qq
        return q.normalise()

    def slerp(self,*args):
        if len(args) == 1:
            q = Quaternion(1,0,0,0)
            qq = self
            t = args[0]
        else:
            q = self
            qq = args[0]
            t = args[1]
        if (q + qq).len() == 0:
            qq = Quaternion(q.x,-q.w,q.z,-q.y)
            t *= 2
        elif (q - qq).len() == 0:
            return q
        ca = q.dot(qq)
        sa = math.sqrt(1 - ca ** 2)
        if sa == 0:
            return q
        a = math.acos(ca)
        sa = math.sin(a*t)/sa
        return (math.cos(a*t) - ca*sa)*q + sa*qq

    def make_slerp(self,*args):
        if len(args) == 0:
            q = Quaternion(1,0,0,0)
            qq = self
        else:
            q = self
            qq = args[0]
        q = q.normalise()
        qq = qq.normalise()
        if (q + qq).len() == 0:
            qq,f = Quaternion(q.y,-q.x,q.w,-q.z),2
        elif (q - qq).len() == 0:
            return lambda t: q
        else:
            f = 1
        ca = q.dot(qq)
        sa = math.sqrt(1 - ca**2)
        if sa == 0:
            return lambda t: q
        a = math.acos(ca)
        qq = (qq - ca*q)/sa
        return lambda t: math.cos(a*f*t)*q + math.sin(a*f*t)*qq
            
    def tomatrixleft(self):
        q = self.normalise()
        a,b,c,d = q.w,q.x,q.y,q.z
        ab,ac,ad,bb,bc,bd,cc,cd,dd = 2*a*b, 2*a*c, 2*a*d, 2*b*b, 2*b*c, 2*b*d, 2*c*c, 2*c*d, 2*d*d
        return [
            1 - cc - dd, bc - ad, ac + bd, 0,
            bc + ad, 1 - bb - dd, cd - ab, 0,
            bd - ac, cd + ab, 1 - bb - cc, 0,
            0,0,0,1
        ]
    
    def tomatrixright(self):
        q = self.normalise()
        a,b,c,d = q.w,-q.x,-q.y,-q.z
        ab,ac,ad,bb,bc,bd,cc,cd,dd = 2*a*b, 2*a*c, 2*a*d, 2*b*b, 2*b*c, 2*b*d, 2*c*c, 2*c*d, 2*d*d
        return [
            1 - cc - dd, bc - ad, ac + bd, 0,
            bc + ad, 1 - bb - dd, cd - ab, 0,
            bd - ac, cd + ab, 1 - bb - cc, 0,
            0,0,0,1
        ]

    def tomatrix(self):
        return self.tomatrixright()


    def vector(self):
        return lib.vectors.vec3.Vec3(self.x,self.y,self.z)

    def real(self):
        return self.w
    
def qRotation(a,*args):
    if len(args) == 3:
        u = lib.vectors.vec3.Vec3(args[0],args[1],args[2])
    else:
        u = args[0]
    q = u.toQuaternion().normalise()
    if q == Quaternion(1,0,0,0):
        return q
    return q.__mul__(math.sin(a/2)).__add__(math.cos(a/2))

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
