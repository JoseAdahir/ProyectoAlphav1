import os
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


import math

import numpy as np

#Despues de inicializar la pantalla utilizar pygame.mouse.set_visible(False) para esconder el mouse
#No se incluye en la clase para evitar errores, asi se puede declarar un objeto tipo fps_camera en cualquier momento

class fps_camera:
    def __init__(self, x, z, height, screen_w, screen_h, tx, ty):
        """X, Z es su posicion inicial en el espacio, height es su coordenada Y/altura, screen_w y screen_h es para poder enfocar el mouse en el centro de la ventana"""
        self.radioColi = 4
        self.EYE_X = x
        self.EYE_Y = height
        self.EYE_Z = z
        self.VEC_X = 0
        self.VEC_Y = 1
        self.VEC_Z = 0
        self.CENTER_X = x
        self.CENTER_Y = height
        self.CENTER_Z = z
        self.PLAYER_H = height
        self.WIDTH = screen_w
        self.HEIGHT = screen_h
        self.theta_x = tx
        self.theta_y = ty
        self.timer = 0
        self.eyes = True #true = ojos abiertos, false = ojos cerrados
        self.pressedKeyq = False
        self.pressedKeye = False
        self.VEC_X_alt = 0
        self.VEC_Z_alt = 0
        self.vectorX = 0
        self.vectorZ = 0
        self.vertexCoords = [  
                   1,1,1,   1,1,-1,   1,-1,-1,   1,-1,1,
                  -1,1,1,  -1,1,-1,  -1,-1,-1,  -1,-1,1  ]
        
        self.elementArray = [ 
                  0,1,2,3, 0,3,7,4, 0,4,5,1,
                  6,2,1,5, 6,5,4,7, 6,7,3,2  ]
        
        self.positions = np.array([[x,height, z],[x, height, z]])

        self.clock = pygame.time.Clock()

    def lookat(self):
        """no es necesario llamar esta funcion en algun momento, consideralo privado"""
        
        self.VEC_X = (math.cos(math.radians(self.theta_x)) + math.sin(math.radians(self.theta_x)))
        self.VEC_Z = (-math.sin(math.radians(self.theta_x)) + math.cos(math.radians(self.theta_x)))
        self.VEC_Y = math.sin(math.radians(self.theta_y))
        
        self.CENTER_X = self.EYE_X + self.VEC_X
        self.CENTER_Z = self.EYE_Z + self.VEC_Z
        self.CENTER_Y = self.EYE_Y + self.VEC_Y
        
    def blink(self):
        glPushMatrix()
        glTranslate(self.EYE_X,self.EYE_Y,self.EYE_Z)
        if self.eyes == False:
            glColor3f(0.0,0.0,0.0)
        else:
            glColor3f(1.0,1.0,1.0)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(3, GL_FLOAT, 0, self.vertexCoords)
        glDrawElements(GL_QUADS, 24, GL_UNSIGNED_INT, self.elementArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glPopMatrix()
        self.timer-=0.1
    
    def update(self):
        """Usar esta funcion dentro del ciclo while not done, solo es necesario llamar esta funcion y se encarga del resto menos cerrar la ventana
        Es necesario implementar una forma de detener el programa por medio de teclas ya que este fija el mouse en el centro de la ventana"""
        self.clock.tick(60)
        for event in pygame.event.get():
            
            i, j = pygame.mouse.get_rel()
            self.theta_x -= i
            self.theta_y -= j

            if self.theta_y > 90:
                self.theta_y = 90
            elif self.theta_y < -90:
                self.theta_y = -90
        

        pressed = pygame.key.get_pressed()
        self.vectorX = 0
        self.vectorZ = 0
        if pressed[pygame.K_w]:
            self.EYE_X = (self.EYE_X+self.VEC_X*0.7)
            self.EYE_Z = (self.EYE_Z+self.VEC_Z*0.7)
            self.vectorX += self.VEC_X*0.7
            self.vectorZ += self.VEC_Z*0.7
        if pressed[pygame.K_s]:
            self.VEC_X*=-1
            self.VEC_Z*=-1
            self.EYE_X = (self.EYE_X+self.VEC_X*0.7)
            self.EYE_Z = (self.EYE_Z+self.VEC_Z*0.7)
            self.vectorX += self.VEC_X*0.7
            self.vectorZ += self.VEC_Z*0.7
 
        if pressed[pygame.K_d]:
            self.VEC_X_alt = (math.cos(math.radians(self.theta_x-90)) + math.sin(math.radians(self.theta_x-90)))*0.7
            self.VEC_Z_alt = (-math.sin(math.radians(self.theta_x-90)) + math.cos(math.radians(self.theta_x-90)))*0.7
            self.EYE_X = (self.EYE_X + self.VEC_X_alt)
            self.EYE_Z = (self.EYE_Z + self.VEC_Z_alt)
            self.vectorX += self.VEC_X_alt
            self.vectorZ += self.VEC_Z_alt
        if pressed[pygame.K_a]:
            self.VEC_X_alt = (math.cos(math.radians(self.theta_x+90)) + math.sin(math.radians(self.theta_x+90)))*0.7
            self.VEC_Z_alt = (-math.sin(math.radians(self.theta_x+90)) + math.cos(math.radians(self.theta_x+90)))*0.7
            self.EYE_X = (self.EYE_X + self.VEC_X_alt)
            self.EYE_Z = (self.EYE_Z + self.VEC_Z_alt)
            self.vectorX += self.VEC_X_alt
            self.vectorZ += self.VEC_Z_alt

        if pressed[pygame.K_q]:
            self.theta_x+=3.5

        if pressed[pygame.K_e]:
            self.theta_x-=3.5

        if self.theta_x > 360:
            self.theta_x = 0
        elif self.theta_x < -360:
            self.theta_x = 0

        if pressed[pygame.K_r]:
            if not self.pressedKeyq:
                self.timer = 2
                self.eyes = not self.eyes
                if(self.eyes):
                    self.positions[1,0]=self.EYE_X
                    self.positions[1,1]=self.EYE_Y
                    self.positions[1,2]=self.EYE_Z
                    self.EYE_X = self.positions[0,0]
                    self.EYE_Y = self.positions[0,1]
                    self.EYE_Z = self.positions[0,2]
                else:
                    self.positions[0,0]=self.EYE_X
                    self.positions[0,1]=self.EYE_Y
                    self.positions[0,2]=self.EYE_Z
                    self.EYE_X = self.positions[1,0]
                    self.EYE_Y = self.positions[1,1]
                    self.EYE_Z = self.positions[1,2]
            self.pressedKeyq = True
        if not pressed[pygame.K_r]:
            self.pressedKeyq = False
        if pressed[pygame.K_t]:
            if not self.pressedKeye:
                print(self.EYE_X)
                print(self.EYE_Z)
            self.pressedKeye=True
        if not pressed[pygame.K_t]:
            self.pressedKeye=False
        self.lookat()
        pygame.mouse.set_pos(self.WIDTH/2, self.HEIGHT/2)
        
    def updateNoBlink(self):
        self.clock.tick(60)
        for event in pygame.event.get():
            i, j = pygame.mouse.get_rel()
            self.theta_x -= i
            self.theta_y -= j
            if self.theta_y > 90:
                self.theta_y = 90
            elif self.theta_y < -90:
                self.theta_y = -90
        pressed = pygame.key.get_pressed()
        self.vectorX = 0
        self.vectorZ = 0
        if pressed[pygame.K_w]:
            self.EYE_X = (self.EYE_X+self.VEC_X*0.7)
            self.EYE_Z = (self.EYE_Z+self.VEC_Z*0.7)
            self.vectorX += self.VEC_X*0.7
            self.vectorZ += self.VEC_Z*0.7
        if pressed[pygame.K_s]:
            self.VEC_X*=-1
            self.VEC_Z*=-1
            self.EYE_X = (self.EYE_X+self.VEC_X*0.7)
            self.EYE_Z = (self.EYE_Z+self.VEC_Z*0.7)
            self.vectorX += self.VEC_X*0.7
            self.vectorZ += self.VEC_Z*0.7
 
        if pressed[pygame.K_d]:
            self.VEC_X_alt = (math.cos(math.radians(self.theta_x-90)) + math.sin(math.radians(self.theta_x-90)))*0.7
            self.VEC_Z_alt = (-math.sin(math.radians(self.theta_x-90)) + math.cos(math.radians(self.theta_x-90)))*0.7
            self.EYE_X = (self.EYE_X + self.VEC_X_alt)
            self.EYE_Z = (self.EYE_Z + self.VEC_Z_alt)
            self.vectorX += self.VEC_X_alt
            self.vectorZ += self.VEC_Z_alt
        if pressed[pygame.K_a]:
            self.VEC_X_alt = (math.cos(math.radians(self.theta_x+90)) + math.sin(math.radians(self.theta_x+90)))*0.7
            self.VEC_Z_alt = (-math.sin(math.radians(self.theta_x+90)) + math.cos(math.radians(self.theta_x+90)))*0.7
            self.EYE_X = (self.EYE_X + self.VEC_X_alt)
            self.EYE_Z = (self.EYE_Z + self.VEC_Z_alt)
            self.vectorX += self.VEC_X_alt
            self.vectorZ += self.VEC_Z_alt
        if pressed[pygame.K_q]:
            self.theta_x+=3.5
        if pressed[pygame.K_e]:
            self.theta_x-=3.5
        if self.theta_x > 360:
            self.theta_x = 0
        elif self.theta_x < -360:
            self.theta_x = 0
        if pressed[pygame.K_t]:
            if not self.pressedKeye:
                print(self.EYE_X)
                print(self.EYE_Z)
            self.pressedKeye=True
        if not pressed[pygame.K_t]:
            self.pressedKeye=False
        self.lookat()
        pygame.mouse.set_pos(self.WIDTH/2, self.HEIGHT/2)
        
    def render2D(self):
        if self.timer > 0:
            self.blink()
    
    def getEyes(self):
        return self.eyes