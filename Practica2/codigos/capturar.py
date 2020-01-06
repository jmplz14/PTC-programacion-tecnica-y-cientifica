# -*- coding: utf-8 -*-
from joblib import load
"""
    Vrep y OpenCV en Python
    Codigo escrito por Glare
    www.robologs.net
    Modificado para practica PCT por Eugenio Aguirre
    Leemos datos de laser, los mostramos con matplot y los salvamos a un fichero JSON
    Importante: La escena tiene que estar ejecutándose en el simulador (Usar botón PLAY)
"""
import vrep
import sys
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import json
import os
import glob

def realizarConexion():
    vrep.simxFinish(-1) #Terminar todas las conexiones
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) #Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)
     
    if clientID!=-1:
        print ('Conexion establecida')
        return clientID
    else:
        sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.") #Terminar este script
    
def iniciarCamaraLaser(clientID):
     #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    return camhandle

def pedirNombresFicheros():
    nombre = ""
    nombre = input("Introzuca el nombre de los ficheros: ")
    
    while len(nombre) == 0:
        nombre = input("Se paso un nobmre no valido. Vuelva a intentarlo: ")
        
    # mostramos el directorio de trabajo y vemos si existe el dir para salvar los datos
    print("Directorio de trabajo es: ", os.getcwd())
    
    directorio = ""
    directorio = input("Introzuca el nombre del directorio: ")
    
    while len(directorio) == 0:
        directorio = input("Se paso un nobmre no valido. Vuelva a intentarlo: ")
        
    listaDir=sorted(glob.glob(directorio+'*'))
    
    nuevoDir=directorio+str(len(listaDir))
    
    if (os.path.isdir(nuevoDir)):
        sys.exit("Error: ya existe el directorio "+ nuevoDir)
    else:
        os.mkdir(nuevoDir)
        os.chdir(nuevoDir)
        print("Cambiando el directorio de trabajo: ", os.getcwd())
        
    return nombre
def iniciarGrafica():
    plt.axis('equal')
    plt.axis([0, 4, -2, 2])  
    
def obtenerPuntosXY(clientID):
     puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
     puntosy=[]
     #puntosz=[]
     returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
     #esperamos un tiempo para que el ciclo de lectura de datos no sea muy rápido
     datosLaser=vrep.simxUnpackFloats(signalValue)
     for indice in range(0,len(datosLaser),3):
         puntosx.append(datosLaser[indice+1])
         puntosy.append(datosLaser[indice+2])
         #puntosz.append(datosLaser[indice])
     return puntosx,puntosy
 
def dibujarGrafica(puntosx, puntosy):
    plt.clf()    
    plt.plot(puntosx, puntosy, 'r.')
    plt.show()
    
def obtenerImage(clientID):
    #Guardar frame de la camara, rotarlo y convertirlo a BGR
    _, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
    img = np.array(image, dtype = np.uint8)
    img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img,2)
    img = np.fliplr(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    #Mostrar frame y salir con "ESC"
    cv2.imshow('Image', img)
    
    return img
def actualizarAñadirDatos(clientID, nombre, ficheroLaser, segudnos, maxIter):
    
    iniciarGrafica()
    iteracion=0
    seguir=True
    
    while(iteracion<maxIter and seguir):
       
        puntosx,puntosy = obtenerPuntosXY(clientID)
        time.sleep(segundos) 
        print("Iteración: ", iteracion)        
        dibujarGrafica(puntosx,puntosy)
        
        #Guardamos los puntosx, puntosy en el fichero JSON
        lectura={"Iteracion":iteracion, "PuntosX":puntosx, "PuntosY":puntosy}
        #ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
        ficheroLaser.write(json.dumps(lectura)+'\n')
        
        img = obtenerImage(clientID, )
        
        if iteracion == 0:
            cv2.imwrite(nombre+str(iteracion + 1)+'.jpg', img)
            
            
        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            seguir=False
        
        iteracion=iteracion+1
        
    #salvo a disco la ultima imagen
    cv2.imwrite(nombre+str(iteracion)+'.jpg', img)
    return iteracion
def detenerSimulacion(clientID):
    #detenemos la simulacion
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
    
    #cerramos la conexion
    vrep.simxFinish(clientID)
    
    #cerramos las ventanas
    cv2.destroyAllWindows()    
    
if __name__ == "__main__":
    
    clientID = realizarConexion()    
    #Guardar la referencia al robot
               
    camhandle = iniciarCamaraLaser(clientID)
    
    nombre = pedirNombresFicheros()
    #Creamos el fichero JSON para guardar los datos del laser
    #usamos diccionarios
    segundos=5
    maxIter=5
    
    
    cabecera={"TiempoSleep":segundos,
              "MaxIteraciones":maxIter}
    
    ficheroLaser=open(nombre+".json", "w")
    
    ficheroLaser.write(json.dumps(cabecera)+'\n')
      
    iteraciones = actualizarAñadirDatos(clientID, nombre, ficheroLaser, segundos, maxIter)
     
    time.sleep(1)
    
    detenerSimulacion(clientID)
    
    
    finFichero={"Iteraciones totales":iteraciones}
    #ficheroLaser.write('{}\n'.format(json.dumps(finFichero)))
    ficheroLaser.write(json.dumps(finFichero)+'\n')
    ficheroLaser.close()
    
  
     








    
    
    