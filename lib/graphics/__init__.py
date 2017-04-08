import OpenGL.GL
import OpenGL.GL.shaders
import OpenGL.GLUT
import OpenGL.GLU
import PIL.Image
import lib.vectors.quaternion
import lib.vectors.vec3
import lib.vectors.vec2
import lib.colours
import math
import numpy

ElapsedTime = 0
DeltaTime = 0
Width = 640
Height = 480
Title = 'Python OpenGL'
_defaultStyle = {
    "stroke": True,
    "fill": True,
    "strokeColour": lib.colours.Colour(1,1,1,1),
    "fillColour": lib.colours.Colour(1,1,1,1),
    "strokeWidth": 5,
}
_styles = [_defaultStyle]
_meshes = []

def draw(dt):
    pass

def setup():
    pass

def key(*args):
    pass

def mouse(*args):
    pass

def run():
    global DeltaTime, ElapsedTime
    etime = OpenGL.GLUT.glutGet(OpenGL.GLUT.GLUT_ELAPSED_TIME)
    DeltaTime = etime - ElapsedTime
    ElapsedTime = etime
    OpenGL.GL.glClear(OpenGL.GL.GL_COLOR_BUFFER_BIT | OpenGL.GL.GL_DEPTH_BUFFER_BIT)
 
    OpenGL.GL.glLoadIdentity()
    draw(DeltaTime)
    OpenGL.GLUT.glutSwapBuffers()
        
def initialise(**kwargs):
    global draw, setup, key, mouse, ElapsedTime, _initialised
    if 'draw' in kwargs:
        draw = kwargs['draw']
    if 'setup' in kwargs:
        setup = kwargs['setup']
    if 'key' in kwargs:
        key = kwargs['key']
    if 'mouse' in kwargs:
        mouse = kwargs['mouse']
    OpenGL.GLUT.glutInit()
    OpenGL.GLUT.glutInitDisplayMode(OpenGL.GLUT.GLUT_RGBA | OpenGL.GLUT.GLUT_DOUBLE | OpenGL.GLUT.GLUT_DEPTH)
    OpenGL.GLUT.glutInitWindowSize(Width,Height)
    OpenGL.GLUT.glutInitWindowPosition(200,200)

    window = OpenGL.GLUT.glutCreateWindow(Title)
 
    OpenGL.GLUT.glutDisplayFunc(run)
    OpenGL.GLUT.glutIdleFunc(run)
    OpenGL.GLUT.glutKeyboardFunc(key)
    OpenGL.GLUT.glutMouseFunc(mouse)
    OpenGL.GLUT.glutMotionFunc(mouse)
    InitGL()
    setupLine()
    setup()
    for m in _meshes:
        m.setup()
    ElapsedTime = OpenGL.GLUT.glutGet(OpenGL.GLUT.GLUT_ELAPSED_TIME)
    _initialised = True
    OpenGL.GLUT.glutMainLoop()
        
def InitGL():
    OpenGL.GL.glClearColor(0.0, 0.0, 0.0, 0.0)
    OpenGL.GL.glClearDepth(1.0)
    OpenGL.GL.glDepthFunc(OpenGL.GL.GL_LESS)
    OpenGL.GL.glEnable(OpenGL.GL.GL_DEPTH_TEST)
    OpenGL.GL.glShadeModel(OpenGL.GL.GL_SMOOTH)   
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_PROJECTION)
    OpenGL.GL.glLoadIdentity()
    OpenGL.GLU.gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    OpenGL.GL.glMatrixMode(OpenGL.GL.GL_MODELVIEW)
 
def resetMatrix():
    OpenGL.GL.glLoadIdentity()
def pushMatrix():
    OpenGL.GL.glPushMatrix()
def popMatrix():
    OpenGL.GL.glPopMatrix()

def rotate(*args):
    if isinstance(args[0],lib.vectors.quaternion.Quaternion):
        OpenGL.GL.glMultMatrixf(args[0].tomatrix())
    elif len(args) == 1:
        OpenGL.GL.glRotate(args[0],0,0,1)
    else:
        OpenGL.GL.glRotate(args[0],args[1],args[2],args[3])

def translate(*args):
    if isinstance(args[0],lib.vectors.vec3.Vec3):
        OpenGL.GL.glTranslatef(args[0].x,args[0].y,args[0].z)
    elif isinstance(args[0],lib.vectors.vec2.Vec2):
        OpenGL.GL.glTranslatef(args[0].x,args[0].y,0)
    elif len(args) == 2:
        OpenGL.GL.glTranslatef(args[0],args[1],0)
    else:
        OpenGL.GL.glTranslatef(args[0],args[1],args[2])
        
def scale(*args):
    if isinstance(args[0],lib.vectors.vec3.Vec3):
        OpenGL.GL.glScalef(args[0].x,args[0].y,args[0].z)
    elif isinstance(args[0],lib.vectors.vec2.Vec2):
        OpenGL.GL.glScalef(args[0].x,args[0].y,1)
    elif len(args) == 2:
        OpenGL.GL.glScalef(args[0],args[1],1)
    elif len(args) == 1:
        OpenGL.GL.glScalef(args[0],args[0],args[0])
    else:
        OpenGL.GL.glScalef(args[0],args[1],args[2])
    
def pushStyle():
    _styles.append(list(_styles[-1]))

def popStyle():
    if len(_styles) > 1:
        _styles.pop()

def resetStyle():
    if len(_styles) > 1:
        _styles.pop()
    _styles.append(list(_defaultStyle))

def stroke(*args):
    if len(args) > 0:
        _styles[-1]['stroke'] = True
        _styles[-1]['strokeColour'] = lib.colours.Colour(args[0])
    else:
        return _styles[-1]['strokeColour']

def fill(*args):
    if len(args) > 0:
        _styles[-1]['fill'] = True
        _styles[-1]['fillColour'] = lib.colours.Colour(args[0])
    else:
        return _styles[-1]['fillColour']

def noStroke():
    _styles[-1]['stroke'] = False

def noFill():
    _styles[-1]['fill'] = False

def strokeWidth(*args):
    if len(args) > 0:
        _styles[-1]['stroke'] = True
        _styles[-1]['strokeWidth'] = args[0]
    else:
        return _styles[-1]['strokeWidth']
    
class Mesh:

    def __init__(self):
        _meshes.append(self)
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.colours = []
        self.length = 0
        self.colour = lib.colours.Colour(1,1,1,1)
        self.texture = False

    def draw(self):
        self.setup()
        self.draw()

    def setup(self):
        if self.texture:
            self.setupTexture()
        else:
            self.setupNoTexture()
        self.initialised = True

    def setupTexture(self):
        self.addTexture(self.texture)
        
        VERTEX_SHADER = OpenGL.GL.shaders.compileShader(
            """#version 120
            varying vec4 vColour;
            varying vec3 vNormal;
            varying vec2 vTexCoord;

            void main() {
              gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
              vColour = gl_Color;
              vNormal = gl_Normal;
              vTexCoord = gl_MultiTexCoord0.st;
            }""", OpenGL.GL.shaders.GL_VERTEX_SHADER)
        FRAGMENT_SHADER = OpenGL.GL.shaders.compileShader("""#version 120
        uniform sampler2D texture;
        varying vec4 vColour;
        varying vec3 vNormal;
        varying vec2 vTexCoord;

        void main() {
          vec4 col = texture2D(texture, vTexCoord);
          gl_FragColor = col*vColour;
        }""", OpenGL.GL.shaders.GL_FRAGMENT_SHADER)
        self.shader = OpenGL.GL.shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        ver = []
        self.length = len(self.vertices)
        for i in range(self.length):
            ver.append(self.vertices[i] + self.colours[i] + self.texcoords[i] + self.normals[i])
        self.vbo = OpenGL.arrays.vbo.VBO( numpy.array(ver, 'f' ))
        self.draw = self.drawTexture

    def setupNoTexture(self):
        
        VERTEX_SHADER = OpenGL.GL.shaders.compileShader(
            """#version 120
            varying vec4 vColour;
            varying vec3 vNormal;

            void main() {
              gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
              vColour = gl_Color;
              vNormal = gl_Normal;
            }""", OpenGL.GL.shaders.GL_VERTEX_SHADER)
        FRAGMENT_SHADER = OpenGL.GL.shaders.compileShader("""#version 120
        varying vec4 vColour;
        varying vec3 vNormal;

        void main() {
          gl_FragColor = vColour;
        }""", OpenGL.GL.shaders.GL_FRAGMENT_SHADER)
        self.shader = OpenGL.GL.shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
        ver = []
        self.length = len(self.vertices)
        for i in range(self.length):
            ver.append(self.vertices[i] + self.colours[i] + self.normals[i])
        self.vbo = OpenGL.arrays.vbo.VBO( numpy.array(ver, 'f' ))
        self.draw = self.drawNoTexture
        
    def drawTexture(self):
        OpenGL.GL.shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try: 
                OpenGL.GL.glEnable(OpenGL.GL.GL_TEXTURE_2D)
                OpenGL.GL.glBindTexture(OpenGL.GL.GL_TEXTURE_2D, self.imageID)
                #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
                #glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
                #glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
                OpenGL.GL.glEnableClientState(OpenGL.GL.GL_VERTEX_ARRAY)
                OpenGL.GL.glEnableClientState(OpenGL.GL.GL_COLOR_ARRAY)
                OpenGL.GL.glEnableClientState(OpenGL.GL.GL_NORMAL_ARRAY)
                OpenGL.GL.glEnableClientState(OpenGL.GL.GL_TEXTURE_COORD_ARRAY)
                OpenGL.GL.glVertexPointer(3, OpenGL.GL.GL_FLOAT, 4*12 , self.vbo )
                OpenGL.GL.glColorPointer(4, OpenGL.GL.GL_FLOAT, 4*12  , self.vbo + 3*4 )
                OpenGL.GL.glTexCoordPointer(2, OpenGL.GL.GL_FLOAT, 4*12  , self.vbo + 7*4)
                OpenGL.GL.glNormalPointer(OpenGL.GL.GL_FLOAT, 4*12  , self.vbo + 9*4)
                OpenGL.GL.glDrawArrays(OpenGL.GL.GL_TRIANGLES, 0, self.length)
            finally:
                self.vbo.unbind()
                OpenGL.GL.glDisableClientState(OpenGL.GL.GL_VERTEX_ARRAY)
                OpenGL.GL.glDisableClientState(OpenGL.GL.GL_COLOR_ARRAY)
                OpenGL.GL.glDisableClientState(OpenGL.GL.GL_NORMAL_ARRAY)
                OpenGL.GL.glDisableClientState(OpenGL.GL.GL_TEXTURE_COORD_ARRAY)
        finally:
            OpenGL.GL.shaders.glUseProgram( 0 )

    def drawNoTexture(self):
        OpenGL.GL.shaders.glUseProgram(self.shader)
        try:
            self.vbo.bind()
            try: 
                OpenGL.GL.glEnableClientState(OpenGL.GL.GL_VERTEX_ARRAY)
                OpenGL.GL.glEnableClientState(OpenGL.GL.GL_COLOR_ARRAY)
                OpenGL.GL.glEnableClientState(OpenGL.GL.GL_NORMAL_ARRAY)
                OpenGL.GL.glVertexPointer(3, OpenGL.GL.GL_FLOAT, 4*10 , self.vbo )
                OpenGL.GL.glColorPointer(4, OpenGL.GL.GL_FLOAT, 4*10  , self.vbo + 3*4 )
                OpenGL.GL.glNormalPointer(OpenGL.GL.GL_FLOAT, 4*10  , self.vbo + 7*4)
                OpenGL.GL.glDrawArrays(OpenGL.GL.GL_TRIANGLES, 0, self.length)
            finally:
                self.vbo.unbind()
                OpenGL.GL.glDisableClientState(OpenGL.GL.GL_VERTEX_ARRAY)
                OpenGL.GL.glDisableClientState(OpenGL.GL.GL_COLOR_ARRAY)
                OpenGL.GL.glDisableClientState(OpenGL.GL.GL_NORMAL_ARRAY)
        finally:
            OpenGL.GL.shaders.glUseProgram( 0 )

    def delete(self):
        self.vbo.delete()

    def addTexture(self,image):
        im = PIL.Image.open(image)
        ix = im.size[0]
        iy = im.size[1]
        image = numpy.array(list(im.getdata()), numpy.uint8)
        ID = OpenGL.GL.glGenTextures(1)
        OpenGL.GL.glBindTexture(OpenGL.GL.GL_TEXTURE_2D, ID)
        OpenGL.GL.glPixelStorei(OpenGL.GL.GL_UNPACK_ALIGNMENT,1)
        OpenGL.GL.glTexParameterf(OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_WRAP_S, OpenGL.GL.GL_CLAMP)
        OpenGL.GL.glTexParameterf(OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_WRAP_T, OpenGL.GL.GL_CLAMP)
        OpenGL.GL.glTexParameterf(OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_MAG_FILTER, OpenGL.GL.GL_LINEAR)
        OpenGL.GL.glTexParameterf(OpenGL.GL.GL_TEXTURE_2D, OpenGL.GL.GL_TEXTURE_MIN_FILTER, OpenGL.GL.GL_LINEAR)
        OpenGL.GL.glTexImage2D( OpenGL.GL.GL_TEXTURE_2D, 0, OpenGL.GL.GL_RGB, ix, iy, 0, OpenGL.GL.GL_RGB, OpenGL.GL.GL_UNSIGNED_BYTE, image )
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
            ll = lib.vectors.vec3.Vec3(1,0,0)
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
                    nml = lib.vectors.vec3.Vec3(math.sin(v[0])*math.cos(v[1]),
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
    VERTEX_SHADER = OpenGL.GL.shaders.compileShader(
        """#version 120
        varying vec4 vColour;
        
        void main() {
         gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
         vColour = gl_Color;
        }""", OpenGL.GL.shaders.GL_VERTEX_SHADER)
    FRAGMENT_SHADER = OpenGL.GL.shaders.compileShader("""#version 120
        varying vec4 vColour;

        void main() {
          gl_FragColor = vColour;
        }""", OpenGL.GL.shaders.GL_FRAGMENT_SHADER)
    lineShader = OpenGL.GL.shaders.compileProgram(VERTEX_SHADER,FRAGMENT_SHADER)
    
def line(*args):
    if isinstance(args[0],lib.vectors.vec2.Vec2):
        s = args[0]
        n = 1
    else:
        s = lib.vectors.vec2.Vec2(args[0],args[1])
        n = 2
    if isinstance(args[n],lib.vectors.vec2.Vec2):
        e = args[n]
        n += 1
    else:
        e = lib.vectors.vec2.Vec2(args[n],args[n+1])
        n += 2
    if len(args) < n + 1:
        sc = _styles[-1]['strokeColour']
        ec = _styles[-1]['strokeColour']
    elif len(args) == n + 1:
        sc = args[n]
        ec = args[n]
    else:
        sc = args[n]
        ec = args[n+1]
    nml = (e - s).rotate90().normalise()*_styles[-1]['strokeWidth']/2
    ll = s + nml
    ul = e + nml
    ur = e - nml
    lr = s - nml
    OpenGL.GL.shaders.glUseProgram(lineShader)
    lvbo = OpenGL.arrays.vbo.VBO( numpy.array(
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
            OpenGL.GL.glEnableClientState(OpenGL.GL.GL_VERTEX_ARRAY)
            OpenGL.GL.glEnableClientState(OpenGL.GL.GL_COLOR_ARRAY)
            OpenGL.GL.glVertexPointer(3, OpenGL.GL.GL_FLOAT, 4*7 , lvbo )
            OpenGL.GL.glColorPointer(4, OpenGL.GL.GL_FLOAT, 4*7  , lvbo + 3*4 )
            OpenGL.GL.glDrawArrays(OpenGL.GL.GL_TRIANGLES, 0, 6)
        finally:
            lvbo.unbind()
            OpenGL.GL.glDisableClientState(OpenGL.GL.GL_VERTEX_ARRAY)
            OpenGL.GL.glDisableClientState(OpenGL.GL.GL_COLOR_ARRAY)
    finally:
        OpenGL.GL.shaders.glUseProgram( 0 )
        lvbo.delete()
