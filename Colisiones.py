import math

def cubos(cubos,numCub):
    for i in range(0,numCub-1):
        for j in range(i+1, numCub):
            distancia = math.sqrt((cubos[i].Position[0]-cubos[j].Position[0])**2 + (cubos[i].Position[2]-cubos[j].Position[2])**2 ) 
            if distancia < cubos[i].radioColi*2:#Necesitas las ubiaciones de cada objeto y por ende de preferencia una función
                cubos[i].Direction[0] *= -1.0
                cubos[i].Position[0] += cubos[i].Direction[0]
                cubos[i].Direction[2] *= -1.0
                cubos[i].Position[2] += cubos[i].Direction[2]
                cubos[j].Direction[0] *= -1.0
                cubos[j].Position[0] += cubos[j].Direction[0]
                cubos[j].Direction[2] *= -1.0
                cubos[j].Position[2] += cubos[j].Direction[2]

def cubos_jugador(cubos, jugador ,numCub):
     for j in range(0, numCub):
        distancia = math.sqrt((jugador.EYE_X-cubos[j].Position[0])**2 + (jugador.EYE_Z-cubos[j].Position[2])**2 ) 
        if distancia < cubos[j].radioColi+jugador.radioColi:#Necesitas las ubiaciones de cada objeto y por ende de preferencia una función
            cubos[j].Direction[0] *= -1.0
            cubos[j].Position[0] += cubos[j].Direction[0]
            cubos[j].Direction[2] *= -1.0
            cubos[j].Position[2] += cubos[j].Direction[2]  
      

def muros(muros, jugador):
    for muro in muros:
        deltaXjugador=abs(muro.Position[0] - jugador.EYE_X)
        deltaZjugador= abs(muro.Position[2] - jugador.EYE_Z) 
        if deltaXjugador < muro.colisionX + jugador.radioColi and deltaZjugador < muro.colisionZ + jugador.radioColi:
            return True
            jugador.EYE_Z -= jugador.vectorZ*1.2
            jugador.EYE_X -= jugador.vectorX*1.2
  
  

def muros_cubos(muros, cubos):
    for i in cubos:
        for j in muros:
        # distancia = math.sqrt((camara.EYE_X-cubos[i].Position[0])**2 + (camara.EYE_Z-cubos[i].Position[2])**2 )
            deltaX=abs(j.Position[0] - i.Position[0])
            deltaZ= abs(j.Position[2] - i.Position[2])
            if deltaX < j.colisionX and deltaZ < j.colisionZ + i.radioColi:
                i.Direction[2] *= -1.0
                i.Position[2] += i.Direction[2]
            if deltaX < muros[0].colisionX +i.radioColi and deltaZ < j.colisionZ:
                i.Direction[0] *= -1.0
                i.Position[0] += i.Direction[0]