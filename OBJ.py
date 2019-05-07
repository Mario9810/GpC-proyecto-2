import pygame
from OpenGL.GL import *

def MATS(filename):
    Linger = {}
    kdMT = None
    for line in open(filename, "r"):
        if line.startswith('#'): continue
        Splot = line.split()
        if not Splot: continue
        if Splot[0] == 'newmtl':
            kdMT = Linger[Splot[1]] = {}
        elif kdMT is None:
            raise ValueError, "el archivo .mtl esta malo"
        elif Splot[0] == 'map_Kd':
            
            kdMT[Splot[0]] = Splot[1]
            facess = pygame.image.load(kdMT['map_Kd'])
            image = pygame.image.tostring(facess, 'RGBA', 1)
            Xaxis, Yaxis = facess.get_rect().size
            texid = kdMT['texture_Kd'] = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texid)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER,
                GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER,
                GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, Xaxis, Yaxis, 0, GL_RGBA,
                GL_UNSIGNED_BYTE, image)
        else:
            kdMT[Splot[0]] = map(float, Splot[1:])
    return Linger

class loadObject:
    def __init__(self, filename, swapyz=False):
        self.Naxis = []
        self.vertexs = []
        self.TextureXYZ = []
        self.faces = []

        material = None
        for line in open(filename, "r"):
            if line.startswith('#'): continue
            Splot = line.split()
            if not Splot: continue
            if Splot[0] == 'v':
                v = map(float, Splot[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.vertexs.append(v)
            elif Splot[0] == 'vn':
                v = map(float, Splot[1:4])
                if swapyz:
                    v = v[0], v[2], v[1]
                self.Naxis.append(v)
            elif Splot[0] == 'vt':
                self.TextureXYZ.append(map(float, Splot[1:3]))
            elif Splot[0] in ('usemtl', 'usemat'):
                material = Splot[1]
            elif Splot[0] == 'mtllib':
                self.MT = MATS(Splot[1])
            elif Splot[0] == 'f':
                face = []
                TextureXYZ = []
                norms = []
                for v in Splot[1:]:
                    w = v.split('/')
                    face.append(int(w[0]))
                    if len(w) >= 2 and len(w[1]) > 0:
                        TextureXYZ.append(int(w[1]))
                    else:
                        TextureXYZ.append(0)
                    if len(w) >= 3 and len(w[2]) > 0:
                        norms.append(int(w[2]))
                    else:
                        norms.append(0)
                self.faces.append((face, norms, TextureXYZ, material))
        #we tell opengl we want to enable textures
        self.gl_list = glGenLists(1)
        glNewList(self.gl_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glFrontFace(GL_CCW)
        for face in self.faces:
            vertexs, Naxis, TextureYX, material = face

            MT = self.MT[material]
            if 'texture_Kd' in MT:
                # use diffuse texmap
                glBindTexture(GL_TEXTURE_2D, kdMT['texture_Kd'])
            else:
                # just use diffuse colour
                glColor(*MT['Kd'])

            glBegin(GL_POLYGON)
            for i in range(len(vertexs)):
                if Naxis[i] > 0:
                    glNormal3fv(self.Naxis[Naxis[i] - 1])
                if TextureYX[i] > 0:
                    glTexCoord2fv(self.TextureXYZ[TextureYX[i] - 1])
                glVertex3fv(self.vertexs[vertexs[i] - 1])
            glEnd()
        glDisable(GL_TEXTURE_2D)
        glEndList()
