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

"""
realiza la conexion y devuleve el id para cominicarnos
"""
def realizarConexion():
    vrep.simxFinish(-1) #Terminar todas las conexiones
    clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) #Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)
     
    #si no falla devuleve el ide sino mensaje de error
    if clientID!=-1:
        print ('Conexion establecida')
        return clientID
    else:
        sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.") #Terminar este script

#inicia la camara y el laser para que tengan datos devuelve la camara para obtener imagenes despues
def iniciarCamaraLaser(clientID):
     
    #cargamos datos de imagene y camara
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    _, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
    _, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
    time.sleep(1)
    return camhandle

"""pide el nombre tanto de los ficheros para el json y las imigenes. Tambie pide
el nombre de la carpeta en la que guardaremos y le añade el numero que le corresponda
segun la scarpetas que existan con ese nombre devuelve el nombre del fichero"""
def pedirNombresFicheros():
    #piden el nombre para los ficheors
    nombre = ""
    nombre = input("Introzuca el nombre de los ficheros: ")
    #comprueba que no estan vacios
    while len(nombre) == 0:
        nombre = input("Se paso un nobmre no valido. Vuelva a intentarlo: ")
        
    print("Directorio de trabajo es: ", os.getcwd())
    
    #pedimos el nombre de la carpeta a crear
    directorio = ""
    directorio = input("Introzuca el nombre del directorio: ")
    
    while len(directorio) == 0:
        directorio = input("Se paso un nobmre no valido. Vuelva a intentarlo: ")
    
    #añadimos el numero al directorio
    listaDir=sorted(glob.glob(directorio+'*'))  
    nuevoDir=directorio+str(len(listaDir))
    #reamos el directorio si no existe
    if (os.path.isdir(nuevoDir)):
        sys.exit("Error: ya existe el directorio "+ nuevoDir)
    else:
        os.mkdir(nuevoDir)
        os.chdir(nuevoDir)
        print("Cambiando el directorio de trabajo: ", os.getcwd())
        
    return nombre

#valores para iniciar la grafica
def iniciarGrafica():
    plt.axis('equal')
    plt.axis([0, 4, -2, 2])  

"""
    Obtiene los datos del laser y los devuelve
    Parameters: clientID= id para obtener datos del laser
    Returns: 
        -puntosX: puntos x del laser
        -puntosY: puntos y del laser
        
"""
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

"""
    Dibuja en una grafica los putnos que obtenemos del laser
    Parameters: 
        -puntosX: puntos x del laser
        -puntosY: puntos y del laser
    Returns: 
              
"""
def dibujarGrafica(puntosx, puntosy):
    plt.clf()    
    plt.plot(puntosx, puntosy, 'r.')
    plt.show()

"""
    Obtiene la imagen de la camara y la procesa
    Parameters: clientID= id para obtener datos del laser
    Returns: 
        -img: imagen ya procesada de la camara
        
"""   
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

"""
    La funcion encgarda de obtener los datos del laser y los añade a el ficheor json
    Tambien guarda la imagen.
    Parameters: 
        -clientID= id para obtener datos del laser
        -nombre = nombre de la capeta donde guardamos el json y las imagenes
        -ficheorLare = fichero en el que escibimos los datos del laser
        -segundos: Tiempo que esepra para tomar otra lectura
        -maxIter: numero de iteraciones
        
    Returns: 
        -iteracion devuelve el numero de iteraciones realizadas
        
"""  
def actualizarAñadirDatos(clientID, nombre, ficheroLaser, segundos, maxIter):
    
    iniciarGrafica()
    iteracion=0
    seguir=True
    
    while(iteracion<maxIter and seguir):
        #obtenemos puntos del slaser
        puntosx,puntosy = obtenerPuntosXY(clientID)
        time.sleep(segundos) 
        print("Iteración: ", iteracion)   
        
        #dibujamos las grafica
        dibujarGrafica(puntosx,puntosy)
        
        #Guardamos los puntosx, puntosy en el fichero JSON
        lectura={"Iteracion":iteracion, "PuntosX":puntosx, "PuntosY":puntosy}
        #ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
        ficheroLaser.write(json.dumps(lectura)+'\n')
        
        #obtenemos la imagen y se pondra en la panatalla del simulador
        img = obtenerImage(clientID, )
        if iteracion == 0:
            cv2.imwrite(nombre+str(iteracion + 1)+'.jpg', img)
            
        #cancelar si no queremos continuar
        tecla = cv2.waitKey(5) & 0xFF
        if tecla == 27:
            seguir=False
        
        iteracion=iteracion+1
        
    #salvo a disco la ultima imagen
    cv2.imwrite(nombre+str(iteracion)+'.jpg', img)
    return iteracion

"""
    Detine la simualcion
    Parameters: 
        -clientID= id para obtener datos del laser
        
    Returns: 
        
"""
def detenerSimulacion(clientID):
    #detenemos la simulacion
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
    
    #cerramos la conexion
    vrep.simxFinish(clientID)
    
    #cerramos las ventanas
    cv2.destroyAllWindows()    
    
if __name__ == "__main__":
    #conctamos con el simulador
    clientID = realizarConexion()    
    #iniciamos camara y laser
    camhandle = iniciarCamaraLaser(clientID)
    
    #pedimos nombre de carpeta y ficheros
    nombre = pedirNombresFicheros()

    segundos=5
    maxIter=5
    
    
    cabecera={"TiempoSleep":segundos,
              "MaxIteraciones":maxIter}
    
    #inicamos el fichero
    ficheroLaser=open(nombre+".json", "w")
    
    ficheroLaser.write(json.dumps(cabecera)+'\n')
    #rellenamos datos
    iteraciones = actualizarAñadirDatos(clientID, nombre, ficheroLaser, segundos, maxIter)
     
    time.sleep(1)
    #paramos la simulacion
    detenerSimulacion(clientID)
    
    
    finFichero={"Iteraciones totales":iteraciones}
    #cerramos y guardamos el fichero
    ficheroLaser.write(json.dumps(finFichero)+'\n')
    ficheroLaser.close()
    
  
     








    
    
    