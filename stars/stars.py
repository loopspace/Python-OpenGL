import sys
import lib.graphics as G
import mbhandler
import math
import random
from lib.vectors.vec3 import Vec3, RandomVec3, RandomUnitVec3
from lib.vectors.quaternion import Quaternion, qRotation
from lib.colours import Colour

MB = False

ESCAPE = b'\x1b'

radius = 10
qRot = Quaternion(1,0,0,0)
pos = Vec3(0,0,0)
direction = Vec3(0,0,-1)
speed = 0.01
dspeed = 0.01
score = 0

white = Colour("white")
yellow = Colour("yellow")

def setup():
    global m,gem,gems
    if MB:
        mbhandler.init()
    else:
        global qRte,qEnd
        qRte,qEnd = qpath(qRot)
        
    m = G.Mesh()
    gem = G.Mesh()
    gems = []
    
    m.addSphere(radius = radius, ambient = 1)
    gem.colour = yellow
    gem.addSphere(radius = .01, ambient = .5, size = 5)
    m.texture = "starmap_4k.jpeg"
    for k in range(50):
        v = RandomVec3(radius)
        gems.append(v)
    G.strokeWidth(.01)
    G.stroke(white)


def key(*args):
    print(args)
    if args[0] == ESCAPE:
        m.delete()
        sys.exit()
 

def mouse(*args):
    print(args)
    
def draw(dt):
    global qRot, qRte, qEnd
    global pos
    global direction
    global speed
    global score

    if MB:
        mb = mbhandler.queue.get()
        
        q = Vec3(0,-1,0).rotateTo(Vec3(-mb['accelerometer']['x'],mb['accelerometer']['z'],mb['accelerometer']['y']))
        qRot = q**0.1 * qRot
        if mb['button_a']['pressed']:
            speed += dspeed
        if mb['button_b']['pressed']:
            speed -= dspeed
    else:
        qRot = qRte(G.ElapsedTime)
        if G.ElapsedTime > qEnd:
            qRte, qEnd = qpath(qRot)
            
    speed = max(min(speed,1),0)
    ds = 4/(1 - pos.lenSqr()/radius**2)**2
    pos += (direction*speed*dt/ds) ** ~qRot

    for g in gems:
        if pos.dist(g) < .1:
            score += 1
            v = RandomVec3(radius)
            g.cloneFrom(v)
            print(score)
        
    G.rotate(qRot)
    m.draw()

    G.translate(-pos)
    for g in gems:
        G.pushMatrix()
        G.translate(g)
        gem.draw()
        G.popMatrix()
    
    G.resetMatrix()
    G.line(0,-.1,0,.1)
    G.line(-.1,0,.1,0)
 

def qpath(q):
    qt = qRotation(2*math.pi*random.random(), RandomUnitVec3())
    s = math.acos(q.dot(qt))/2*10000
    sl = q.make_slerp(qt)
    st = G.ElapsedTime
    return lambda t: sl(min(1,(t - st)/s)), st + s

if __name__ == "__main__":
    G.initialise(draw = draw,setup = setup,key = key,mouse = mouse)
