import pygame
from pygame.locals import *

# Cargamos las bibliotecas de OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

import numpy as np
import Colisiones as Cl
# Se carga el archivo de la clase Cubo
import sys
sys.path.append('..')
from Pochita import Pochita
from Muro import Muro
from Cubo import Cubo
from Mapa import Mapa
from Estacion import Estacion
from fps_camera import fps_camera
from Tren import Tren
from skybox import Skybox

screen_width = 800
screen_height = 600
#vc para el obser.
FOVY=60.0
ZNEAR=0.01
ZFAR=900.0
#Variables para definir la posicion del observador
#gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)\
    
#COORDENADAS DE INICIO PARA LA ESTACION DE TREN
# EYE_X =150
# EYE_Y = 7
# EYE_Z = 100.0
timer = 50.0
switched=False

EYE_X = 150
EYE_Y = 7
EYE_Z = 100
CENTER_X = 0
CENTER_Y = 1
CENTER_Z = 0
posX=0
posZ =0
UP_X=0
UP_Y=1
UP_Z=0
#Variables para dibujar los ejes del sistema
X_MIN=-500
X_MAX=500
Y_MIN=-500
Y_MAX=500
Z_MIN=-500
Z_MAX=500
#Dimension del plano
DimBoard = 100

#Variables asociados a los objetos de la clase Cubo
murosEstacion = []
murosMapa2 = []
muro = [] # Crear un muro estático
murosEstacion.append(Muro(102,2,115,102, 2))
murosEstacion.append(Muro(100,2,88,75, 1))
murosEstacion.append(Muro(23,2,95,1, 12))
murosEstacion.append(Muro(180,2,95,1, 12))

murosEstacion.append(Muro(158,2,89,16,1))
murosEstacion.append(Muro(100,2,108,2,2))

#Pilar estación
murosEstacion.append(Muro(126,2,100,1, 1))
murosEstacion.append(Muro(63,2,99,1, 1))



muro.append(Muro(-241,0,-110,1,123))
muro.append(Muro(-195,0,-176,77,1))
#-234, -176 (X1, Z1)
#-157, -176  (X2, Z2)
# punto medio de X= X2 + (X1-X2)/2
muro.append(Muro(-158,0,-170,1,10))
#127 143
#
muro.append(Muro(-142,0,-159,18,1))
muro.append(Muro(-127,0,-143,1,11))
muro.append(Muro(-112,0,-128,12,1))

#pilares
muro.append(Muro(-120,5,-105,2,2))
muro.append(Muro(-120,5,-56,2,2))

muro.append(Muro(-95,5,-80,1,87))
#Inner walls
muro.append(Muro(-160,0,-104.5,0.5,40))
muro.append(Muro(-160,0,-39,0.5,8))
muro.append(Muro(-209,0,-39,0.5,8))
muro.append(Muro(-209,0,-72,0.5,8))
muro.append(Muro(-184,0,-80, 23, 0.5))
muro.append(Muro(-216,0,-64,8,0.5))
muro.append(Muro(-224,0,-47,15,0.5))
muro.append(Muro(-222,0,-79, 0.5, 14))
muro.append(Muro(-208,0,-95,14,0.5))
muro.append(Muro(-175,0,-127,14,0.5))
muro.append(Muro(-191,0,-111,0.5,14))
muro.append(Muro(-151,0,-142,7,0.5))
muro.append(Muro(-144,0,-135,0.5,8))
muro.append(Muro(-152,0,-128,7,0.5))
muro.append(Muro(-152,0,-31,56,0.5))
#-136,7,-134 inicio de mapa 1

murosMapa2.append(Muro(215,0,-177,22,0.5))
murosMapa2.append(Muro(240,0,-151,0.5,22))
murosMapa2.append(Muro(232,0,-126,8,0.5))
murosMapa2.append(Muro(199,0,-126,8,0.5))
murosMapa2.append(Muro(192,0,-168, 0.5,8))
murosMapa2.append(Muro(192,0,-135, 0.5,8))
murosMapa2.append(Muro(183,0,-142, 7, 0.5))
murosMapa2.append(Muro(175,0,-161,15,0.5))
murosMapa2.append(Muro(176,0,-103,0.5,38))
murosMapa2.append(Muro(184,0,-64,8,0.5))
murosMapa2.append(Muro(191,0,-72,0.5,8))
murosMapa2.append(Muro(191,0,-39,0.5,8))
murosMapa2.append(Muro(215,0,-30,24,0.5))
murosMapa2.append(Muro(240,0,-72,0.5,8))
murosMapa2.append(Muro(240,0,-39,0.5,8))
murosMapa2.append(Muro(247,0,-64,8,0.5))
murosMapa2.append(Muro(255,0,-45,16,0.5))
murosMapa2.append(Muro(224,0,-80,28,0.5))
murosMapa2.append(Muro(255,0,-72,0.5,8))
murosMapa2.append(Muro(273,0,-63,0.5,17))
murosMapa2.append(Muro(175,0,-46,12,0.5))
murosMapa2.append(Muro(280,0,-79,6,0.5))
murosMapa2.append(Muro(289,0,-103,0.5,25))
murosMapa2.append(Muro(263,0,-129,19,0.5))
murosMapa2.append(Muro(237,0,-87,0.5,6))
murosMapa2.append(Muro(237,0,-120,0.5,5))
murosMapa2.append(Muro(232,0,-113,5,0.5))
murosMapa2.append(Muro(223,0,-95,17,0.5))
murosMapa2.append(Muro(208,0,-111,0.5,17))
murosMapa2.append(Muro(228,0,-119,0.5,7))
murosMapa2.append(Muro(158,0,-103,0.5,53))
#264 7 -111 inicio mapa 2

mapa = []
pochita = []
estacion = []
tren= []
sky = []

#Inicializacipon de Camara
camara = fps_camera(EYE_X,EYE_Z, EYE_Y, screen_width, screen_height, 0, 0)
pygame.init()
pygame.mixer.init()
#Musica

sonido_fondo1 = pygame.mixer.Sound("snowfall.wav")
sonido_fondo2 = pygame.mixer.Sound("SonicCD.wav")
pygame.mixer.Sound.play(sonido_fondo1)


#iluminacion

posicionytipo= np.array([30.0, 100, 35.0, 1.0] )
colorambiental=np.array([0,0,0,1])
colordifuso=np.array([1.0,1.0,1.0,1] )
colorespecular=np.array([1.0,1.0,1.0,1] )

light_model_ambient=np.array([0.2,0.2,0.2,1])
mat_ambient= np.array([0.6, 0.6, 0.5, 0.4] )
mat_difusse=np.array([1.0,1.0,1.0,1] )
mat_specular=np.array([1.0,1.0,1.0,1] )
mat_emission=np.array([0,0,0,0] )

def Init():
    screen = pygame.display.set_mode(
        (screen_width, screen_height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Fear of night")

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(FOVY, screen_width/screen_height, ZNEAR, ZFAR)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(EYE_X,EYE_Y,EYE_Z,CENTER_X,CENTER_Y,CENTER_Z,UP_X,UP_Y,UP_Z)
    glClearColor(0,0,0,0)
    glEnable(GL_DEPTH_TEST)
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    
    #Niebla
    glEnable(GL_FOG)
    glFogi(GL_FOG_MODE,GL_EXP2)
    glFogfv(GL_FOG_COLOR, [0.5,0.5,0.5,0.01])
    glFogf(GL_FOG_DENSITY, 0.01)
    glHint(GL_FOG_HINT, GL_FASTEST)
 
    #Luz general
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[149/255, 152/255, 127/255, 1.0])
    glLightModelf(GL_LIGHT_MODEL_LOCAL_VIEWER,GL_FALSE)
    glLightModelf(GL_LIGHT_MODEL_TWO_SIDE,GL_FALSE)
    
    #Luces config
    #Luz 0
    glLightfv(GL_LIGHT0, GL_POSITION, posicionytipo)
    glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION,[0,-1,0])
    glLightfv(GL_LIGHT0,GL_SPOT_CUTOFF, 45)
    glLightfv(GL_LIGHT0,GL_SPOT_EXPONENT,1)
    glLightfv(GL_LIGHT0, GL_AMBIENT, colorambiental)
    glLightfv(GL_LIGHT0, GL_DIFFUSE, colordifuso)
    glLightfv(GL_LIGHT0, GL_SPECULAR, colorespecular)
    #Luz 1
    glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 30, 0.0, 1.0] )
    glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION,[0.0,-1.0,0.0])
    glLightfv(GL_LIGHT1,GL_SPOT_CUTOFF,90)
    glLightfv(GL_LIGHT1,GL_SPOT_EXPONENT,1)
    glLightfv(GL_LIGHT1, GL_AMBIENT, [0.0,0.0,0.0,1.0])
    glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.9,0.09,1.0,1])
    glLightfv(GL_LIGHT1, GL_SPECULAR, [0.9,0.9,1.0,1])
    #Luz 2 estacion
    glLightfv(GL_LIGHT2, GL_POSITION, [80.0, 20.0, 89.0, 1.0] )
    glLightfv(GL_LIGHT2, GL_SPOT_DIRECTION,[0.0,-1.0,0.0])
    glLightfv(GL_LIGHT2,GL_SPOT_CUTOFF,90)
    glLightfv(GL_LIGHT2,GL_SPOT_EXPONENT,1)
    glLightfv(GL_LIGHT2, GL_AMBIENT, [47/255,79/255,237/255,1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE, [0.04,0.31,0.65,1])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.35,0.33,0.61,1])
    #Luz 3
    glLightfv(GL_LIGHT3, GL_POSITION, [0.0, 30, -200.0, 1.0] )
    glLightfv(GL_LIGHT3, GL_SPOT_DIRECTION,[0.0,-1.0,0.0])
    glLightfv(GL_LIGHT3,GL_SPOT_CUTOFF,90)
    glLightfv(GL_LIGHT3,GL_SPOT_EXPONENT,1)
    glLightfv(GL_LIGHT3, GL_AMBIENT, [0.52,0.34,0.61,1.0])
    glLightfv(GL_LIGHT3, GL_DIFFUSE, [0.32,0.17,0.30,1])
    glLightfv(GL_LIGHT3, GL_SPECULAR, [0.17,0.30,0.32,1])
    #Luz 4 area 1
    glLightfv(GL_LIGHT4, GL_POSITION, [217.0, 20, -54.0, 1.0] )
    glLightfv(GL_LIGHT4, GL_SPOT_DIRECTION,[0.0,-1.0,0.0])
    glLightfv(GL_LIGHT4,GL_SPOT_CUTOFF,90)
    glLightfv(GL_LIGHT4,GL_SPOT_EXPONENT,1)
    glLightfv(GL_LIGHT4, GL_AMBIENT, [47/255,179/255,23/255,1.0])
    glLightfv(GL_LIGHT4, GL_DIFFUSE, [0.4,0.7,0.6,1])
    glLightfv(GL_LIGHT4, GL_SPECULAR, [0.3,0.5,0.6,1])
    #Luz 5
    glLightfv(GL_LIGHT5, GL_POSITION, [215.0, 20, -151.0, 1.0] )
    glLightfv(GL_LIGHT5, GL_SPOT_DIRECTION,[0.0,-1.0,0.0])
    glLightfv(GL_LIGHT5,GL_SPOT_CUTOFF,90)
    glLightfv(GL_LIGHT5,GL_SPOT_EXPONENT,1)
    glLightfv(GL_LIGHT5, GL_AMBIENT, [1.0,0.20,0.30,1.0])
    glLightfv(GL_LIGHT5, GL_DIFFUSE, [0.9,0.3,0.10,1])
    glLightfv(GL_LIGHT5, GL_SPECULAR, [0.9,0.2,0.10,1])
    #material
    glMaterialfv(GL_FRONT,GL_AMBIENT,mat_ambient)
    glMaterialfv(GL_FRONT,GL_DIFFUSE,mat_difusse)
    glMaterialfv(GL_FRONT,GL_SPECULAR,mat_specular)
    glMaterialfv(GL_FRONT,GL_EMISSION,mat_emission)
    glMaterialfv(GL_FRONT, GL_SHININESS, 5)
    
    
    #Inicialización de objetos
    estacion.append(Estacion(100,-10,100,-90,0,300))
    estacion.append(Estacion(61,-10,43,90,180,300))
    mapa.append(Mapa(200,0.02,-40,270,4,"area1.obj"))
    mapa.append(Mapa(-200,0.02,-40,270,4,"area2.obj"))
    tren.append(Tren(600,-10,78.60,-90,12))
    tren.append(Tren(675,-10,78.60,-90,12))
    tren.append(Tren(750,-10,78.60,-90,12))
    sky.append(Skybox(0,0,0,100))
    for i in range(0,1):
        pochita.append(Pochita(DimBoard, 0.3))

#Se mueve al observador circularmente al rededor del plano XZ a una altura fija (EYE_Y)
def lookat():
    glLoadIdentity()
    if camara.getEyes():
        if Cl.muros(muro, camara):
            camara.EYE_Z -= camara.vectorZ 
            camara.CENTER_Z -= camara.vectorZ
            if Cl.muros(muro, camara):
                camara.EYE_Z += camara.vectorZ 
                camara.CENTER_Z += camara.vectorZ
                camara.EYE_X -= camara.vectorX 
                camara.CENTER_X -= camara.vectorX
                if Cl.muros(muro, camara):
                    camara.EYE_X -= camara.vectorX 
                    camara.CENTER_X -= camara.vectorX
                    camara.EYE_Z -= camara.vectorZ 
                    camara.CENTER_Z -= camara.vectorZ
    else:
        if Cl.muros(murosMapa2, camara):
            camara.EYE_Z -= camara.vectorZ 
            camara.CENTER_Z -= camara.vectorZ
            if Cl.muros(murosMapa2, camara):
                camara.EYE_Z += camara.vectorZ 
                camara.CENTER_Z += camara.vectorZ
                camara.EYE_X -= camara.vectorX 
                camara.CENTER_X -= camara.vectorX
                if Cl.muros(murosMapa2, camara):
                    camara.EYE_X -= camara.vectorX 
                    camara.CENTER_X -= camara.vectorX
                    camara.EYE_Z -= camara.vectorZ 
                    camara.CENTER_Z -= camara.vectorZ 
    gluLookAt(camara.EYE_X,camara.EYE_Y,camara.EYE_Z,camara.CENTER_X,camara.CENTER_Y,camara.CENTER_Z,0,1,0)

def lookatEstación():
    glLoadIdentity()
    if Cl.muros(murosEstacion, camara):
        camara.EYE_Z -= camara.vectorZ 
        camara.CENTER_Z -= camara.vectorZ
        if Cl.muros(murosEstacion, camara):
            camara.EYE_Z += camara.vectorZ 
            camara.CENTER_Z += camara.vectorZ
            camara.EYE_X -= camara.vectorX 
            camara.CENTER_X -= camara.vectorX
            if Cl.muros(murosEstacion, camara):
                camara.EYE_X -= camara.vectorX 
                camara.CENTER_X -= camara.vectorX
                camara.EYE_Z -= camara.vectorZ 
                camara.CENTER_Z -= camara.vectorZ
    gluLookAt(camara.EYE_X,camara.EYE_Y,camara.EYE_Z,camara.CENTER_X,camara.CENTER_Y,camara.CENTER_Z,0,1,0)       

def display(camera):
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glEnable(GL_LIGHT4)
    glEnable(GL_LIGHT5)
    if(camera.getEyes()):
        glEnable(GL_LIGHT0)
    else:
        glEnable(GL_LIGHT1)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    #Se dibuja un esfera para la luz
    glPushMatrix()
    glTranslated(217,20,-54)
    gluSphere(gluNewQuadric(), 3.0, 32, 16)
    glPopMatrix()

    glPushMatrix()
    glTranslated(215,20,-151)
    gluSphere(gluNewQuadric(), 3.0, 32, 16)
    glPopMatrix()
    
    if(camera.getEyes()):
        mapa[1].draw()
        for pochitas in pochita:
            pochitas.update()
            pochitas.draw()
    else:
        mapa[0].draw()
        for pochitas in pochita:
            pochitas.update()
            pochitas.draw()
            
    if(camera.getEyes()):
        glDisable(GL_LIGHT0)
    else:
        glDisable(GL_LIGHT1)
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHT3)
    glDisable(GL_LIGHT4)
    glDisable(GL_LIGHT5)
    glDisable(GL_LIGHTING)
    
def escenaEstación():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glShadeModel(GL_SMOOTH)
    glEnable(GL_LIGHT2)
    glEnable(GL_LIGHT3)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    #Se dibuja el plano verde
    glPushMatrix()
    glTranslated(0,-12,0)
    glNormal3f(0,1,0)
    glColor3f(45/255, 87/255, 44/255)
    glBegin(GL_QUADS)
    glVertex3d(-DimBoard, 0, -DimBoard)
    glVertex3d(-DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, DimBoard)
    glVertex3d(DimBoard, 0, -DimBoard)
    glEnd()
    glPopMatrix()
    
    for estaciones in estacion:
        estaciones.draw()
    for trenes in tren:
        trenes.update()
        trenes.draw()
    sky[0].draw()
    glDisable(GL_LIGHT2)
    glDisable(GL_LIGHT3)
    glDisable(GL_LIGHTING)


done = False
Init()
#Escena tren
for i in range(0,700):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                print("Se acabo")
                exit(0)
    camara.updateNoBlink()
    lookatEstación()
    escenaEstación()
    pygame.display.flip()
#Se cambian las variables del jugador al cambio de escena
camara.timer=2
camara.EYE_X = -136
camara.EYE_Z = -134
camara.positions[0,0]=-136
camara.positions[0,2]=-134
camara.positions[1,0]=264
camara.positions[1,2]=-111
switched=True
#Se detiene el sonido de fondo y se cambia
pygame.mixer.Sound.stop(sonido_fondo1)
pygame.mixer.Sound.play(sonido_fondo2,-1)
#Cambio a luz ambiental amarilla 
glLightModelfv(GL_LIGHT_MODEL_AMBIENT,[249/255, 252/255, 227/255, 1.0])
while not done:
    
    # Cl.cubos(pochita, 3)
    Cl.muros_cubos(muro, pochita)
    # Cl.cubos_jugador(cubos, camara ,ncubos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                done = True
    camara.update()
    lookat()
    display(camara)
    camara.render2D()
    pygame.display.flip()

pygame.quit()