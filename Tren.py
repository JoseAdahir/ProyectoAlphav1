import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from objloader import *

 
class Tren:
    
    def __init__(self,x,y,z,ang, tam):
        self.tam = tam
        self.ang = ang
        self.obj = OBJ("2te116.obj", swapyz = True)
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
    
    def update(self):
        if(self.Position[0]>-2500):
            self.Position[0] = self.Position[0] - 6
        else:
            self.Position[0]=self.x+2500
            

    def draw(self):
        glPushMatrix()
        glTranslatef(self.Position[0], self.Position[1], self.Position[2])
        glScaled(self.tam, 1.3*self.tam, self.tam)  # Cambia las dimensiones del muro a 10x10
        glRotated(self.ang, 1,0,0)
        glRotated(90, 0,0,1)
        self.obj.render()

        glPopMatrix()