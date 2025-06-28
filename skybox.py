import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from objloader import *

class Skybox:
    
    def __init__(self,x,y,z,tam):
        self.tam = tam
        self.obj = OBJ("skybox.obj", swapyz = True)
        self.obj.generate()
        self.x=x
        self.y=y
        self.z =z

    def draw(self):
        glPushMatrix()
        glTranslatef(self.x, self.y, self.z)
        glScaled(4*self.tam, 4*self.tam, 3*self.tam)
        self.obj.render()

        glPopMatrix()