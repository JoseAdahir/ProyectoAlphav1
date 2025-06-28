import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from objloader import *


class Estacion:
    
    def __init__(self,x,y,z,ang, ang2, tam):
        self.tam = tam
        self.angX = ang
        self.angY = ang2
        self.obj = OBJ("nuevaestacion.obj", swapyz = True)
        self.obj.generate()
    
        self.colisionX=30
        self.colisionZ=30
        self.x=x
        self.y=y
        self.z =z
        self.ang = ang
        
        #Se inicializa una posicion aleatoria en el tablero
        self.Position = []
        self.Position.append(x)
        self.Position.append(y)
        self.Position.append(z)

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(4*self.tam, 4*self.tam, 3*self.tam)  # Cambia las dimensiones del muro a 10x10
        glRotated(self.angX, 1,0,0)
        glRotated(self.angY, 0,1,0)
        self.obj.render()

        glPopMatrix()