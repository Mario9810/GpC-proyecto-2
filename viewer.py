import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OBJ import *

pygame.init()
viewport = (1280,720)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)

glLightfv(GL_LIGHT0, GL_POSITION,  (-30,190, 150, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 2.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           
obj = loadObject(sys.argv[1], swapyz=True)
clock = pygame.time.Clock()
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 300.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
rx, ry = (0,0)
tx, ty = (0,0)
rz = 5
rotate = move = False
while 1:
    clock.tick(28)
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_ESCAPE:
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4: rz = max(1, rz-1)
            elif event.button == 5: rz +=1
        
        
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 4: zpos = max(1, zpos-1)
            elif event.button == 5: zpos += 1
            elif event.button == 1: rotate = True
            elif event.button == 3: move = True
            
        elif event.type == MOUSEBUTTONUP:
            if event.button == 1: rotate = False
            elif event.button == 3: move = False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                rotate = move = True
                rx = rx - 8
                rotate = move = False
                
            elif event.key == pygame.K_RIGHT:
                rotate = move = True
                rx = rx + 8
                rotate = move = False
            elif event.key == pygame.K_UP:
                rotate = move = True
                ry = ry + 8
                rotate = move = False
            elif event.key == pygame.K_DOWN:
                rotate = move = True
                ry = ry - 8
                rotate = move = False
            elif event.key == pygame.K_s:
                rotate = move = True
                ty = ty + 75
                rotate = move = False
            elif event.key == pygame.K_w:
                rotate = move = True
                ty = ty - 75
                rotate = move = False
            elif event.key == pygame.K_a:
                rotate = move = True
                tx = tx + 75
                rotate = move = False
            elif event.key == pygame.K_d:
                rotate = move = True
                tx = tx - 75
                rotate = move = False
                
                
            
        
        elif event.type == MOUSEMOTION:
            i, j = event.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j
        
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslate(tx/20., ty/20., - rz)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    glCallList(obj.gl_list)

    pygame.display.flip()
