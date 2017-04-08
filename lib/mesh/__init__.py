from OpenGL.GL import *
from OpenGL.GL import shaders
from OpenGL.arrays import vbo
from numpy import array, uint8
from PIL.Image import open
import math
import lib.vectors.vec3 as vec3
import lib.vectors.vec2 as vec2
import lib.colours

class Mesh:

    def __init__(self):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.colours = []
        self.length = 0
        self.colour = lib.colours.Colour(1,1,1,1)
        self.texture = False

    def setup(self):
        if self.texture:
            self.setupTexture()
        else:
            self.setupNoTexture()

    def setupTexture(self):
        self.addTexture(self.texture)
        
        VERTEX_SHADER = shaders.compileShader(
            """#version 120
            varying vec4 vColour;
            varying vec3 vNormal;
            varying vec2 vTexCoord;

            void main() {
              gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
              vColour = gl_Color;
              vNormal = gl_Normal;
              vTexCoord = gl_MultiTexCoord0.st;
            }""", GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader("""#version 120
        uniform sampler2D texture;
        varying vec4 vColour;
        varying vec3 vNormal;
        varying vec2 vTexCoord;

        void main() {
          vec4 col = texture2D(texture, vTexCoord);
          gl_FragColor = col*vColour;
        }""", GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        ver = []
        self.length = len(self.vertices)
        for i in range(self.length):
            ver.append(self.vertices[i] + self.colours[i] + self.texcoords[i] + self.normals[i])
        self.vbo = vbo.VBO( array(ver, 'f' ))
        self.draw = self.drawTexture

    def setupNoTexture(self):
        
        VERTEX_SHADER = shaders.compileShader(
            """#version 120
            varying vec4 vColour;
            varying vec3 vNormal;

            void main() {
              gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
              vColour = gl_Color;
              vNormal = gl_Normal;
            }""", GL_VERTEX_SHADER)
        FRAGMENT_SHADER = shaders.compileShader("""#version 120
        varying vec4 vColour;
        varying vec3 vNormal;

        void main() {
          gl_FragColor = vColour;
        }""", GL_FRAGMENT_SHADER)
        self.shader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        ver = []
        self.length = len(self.vertices)
        for i in range(self.length):
            ver.append(self.vertices[i] + self.colours[i] + self.normals[i])
        self.vbo = vbo.VBO( array(ver, 'f' ))
        self.draw = self.drawNoTexture
        
    def drawTexture(self):
        shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try: 
                glEnable(GL_TEXTURE_2D)
                glBindTexture(GL_TEXTURE_2D, self.imageID)
                #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
                glEnableClientState(GL_VERTEX_ARRAY)
                glEnableClientState(GL_COLOR_ARRAY)
                glEnableClientState(GL_NORMAL_ARRAY)
                glEnableClientState(GL_TEXTURE_COORD_ARRAY)
                glVertexPointer(3, GL_FLOAT, 4*12 , self.vbo )
                glColorPointer(4, GL_FLOAT, 4*12  , self.vbo + 3*4 )
                glTexCoordPointer(2, GL_FLOAT, 4*12  , self.vbo + 7*4)
                glNormalPointer(GL_FLOAT, 4*12  , self.vbo + 9*4)
                glDrawArrays(GL_TRIANGLES, 0, self.length)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)
                glDisableClientState(GL_NORMAL_ARRAY)
                glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        finally:
            shaders.glUseProgram( 0 )

    def drawNoTexture(self):
        shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try: 
                glEnableClientState(GL_VERTEX_ARRAY)
                glEnableClientState(GL_COLOR_ARRAY)
                glEnableClientState(GL_NORMAL_ARRAY)
                glVertexPointer(3, GL_FLOAT, 4*10 , self.vbo )
                glColorPointer(4, GL_FLOAT, 4*10  , self.vbo + 3*4 )
                glNormalPointer(GL_FLOAT, 4*10  , self.vbo + 7*4)
                glDrawArrays(GL_TRIANGLES, 0, self.length)
            finally:
                self.vbo.unbind()
                glDisableClientState(GL_VERTEX_ARRAY)
                glDisableClientState(GL_COLOR_ARRAY)
                glDisableClientState(GL_NORMAL_ARRAY)
        finally:
            shaders.glUseProgram( 0 )

    def delete(self):
        self.vbo.delete()

    def addTexture(self,image):
        im = open(image)
        ix = im.size[0]
        iy = im.size[1]
        image = array(list(im.getdata()), uint8)
        ID = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, ID)
        glPixelStorei(GL_UNPACK_ALIGNMENT,1)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexImage2D( GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGB, GL_UNSIGNED_BYTE, image )
        self.imageID = ID

    def addSphere(self,**kwargs):
        r = kwargs['radius']
        if 'ambient' in kwargs:
            am = kwargs['ambient']
        else:
            am = 0
        if 'lighting' in kwargs:
            ll = kwargs['lighting'].normalise()
        else:
            ll = vec3.Vec3(1,0,0)
        if 'size' in kwargs:
            np = kwargs['size']
            nt = 2*np
        else:
            nt = 20
            np = 10
        st = 0
        et = math.pi
        dt = (et-st)/nt
        sp = 0
        ep = 2*math.pi
        dp = (ep - sp)/np
        for i in range(nt):
            theta = st + (i+1)*dt
            ptheta = st + i*dt
            for j in range(np):
                phi = sp + (j+1)*dp
                pphi = sp + j*dp
                ver = []
                tex = []
                for v in [
                        [ptheta,pphi],
                        [ptheta,phi],
                        [theta,phi],
                        [theta,phi],
                        [ptheta,pphi],
                        [theta,pphi]
                ]:
                    self.vertices.append([
                        r*math.sin(v[0])*math.cos(v[1]),
                        r*math.sin(v[0])*math.sin(v[1]),
                        r*math.cos(v[0])
                        ])
                    nml = vec3.Vec3(math.sin(v[0])*math.cos(v[1]),
                        math.sin(v[0])*math.sin(v[1]),
                        math.cos(v[0]))
                    t = am+(1 - am)*max(0,ll.dot(nml))
                    self.colours.append(self.colour.shade(t).tolist())
                    self.normals.append([nml.x,nml.y,nml.z])
                    self.texcoords.append(
                        [(v[1] - sp)/ep,
                         (v[0] - st)/et
                        ])




def setupLine():
    global lineShader
    VERTEX_SHADER = shaders.compileShader(
        """#version 120
        varying vec4 vColour;
        
        void main() {
         gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
         vColour = gl_Color;
        }""", GL_VERTEX_SHADER)
    FRAGMENT_SHADER = shaders.compileShader("""#version 120
        varying vec4 vColour;

        void main() {
          gl_FragColor = vColour;
        }""", GL_FRAGMENT_SHADER)
    lineShader = shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
    
def line(*args):
    if isinstance(args[0],vec2.Vec2):
        s = args[0]
        n = 1
    else:
        s = vec2.Vec2(args[0],args[1])
        n = 2
    if isinstance(args[n],vec2.Vec2):
        e = args[n]
        n += 1
    else:
        e = vec2.Vec2(args[n],args[n+1])
        n += 2
    if len(args) < n + 1:
        sc = [1,1,1,1]
        ec = [1,1,1,1]
    elif len(args) == n + 1:
        sc = args[n]
        ec = args[n]
    else:
        sc = args[n]
        ec = args[n+1]
    nml = (e - s).rotate90().normalise()*0.001
    ll = s + nml
    ul = e + nml
    ur = e - nml
    lr = s - nml
    shaders.glUseProgram(lineShader)
    lvbo = vbo.VBO( array(
        [ll.x,ll.y,-1] + sc.tolist() +
        [ul.x,ul.y,-1] + ec.tolist() +
        [lr.x,lr.y,-1] + sc.tolist() +
        [ul.x,ul.y,-1] + ec.tolist() +
        [lr.x,lr.y,-1] + sc.tolist() +
        [ur.x,ur.y,-1] + ec.tolist(), 'f')
        )
    try:
        lvbo.bind()
        try: 
            glEnableClientState(GL_VERTEX_ARRAY)
            glEnableClientState(GL_COLOR_ARRAY)
            glVertexPointer(3, GL_FLOAT, 4*7 , lvbo )
            glColorPointer(4, GL_FLOAT, 4*7  , lvbo + 3*4 )
            glDrawArrays(GL_TRIANGLES, 0, 6)
        finally:
            lvbo.unbind()
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_COLOR_ARRAY)
    finally:
        shaders.glUseProgram( 0 )
        lvbo.delete()
