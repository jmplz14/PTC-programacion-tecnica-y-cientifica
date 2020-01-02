# -*- coding: utf-8 -*-
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


vrep.simxFinish(-1) #Terminar todas las conexiones
clientID=vrep.simxStart('127.0.0.1',19999,True,True,5000,5) #Iniciar una nueva conexion en el puerto 19999 (direccion por defecto)
 
if clientID!=-1:
    print ('Conexion establecida')
else:
    sys.exit("Error: no se puede conectar. Tienes que iniciar la simulación antes de llamar a este script.") #Terminar este script
 
#Guardar la referencia al robot

_, robothandle = vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx', vrep.simx_opmode_oneshot_wait)
        
#Guardar la referencia de los motores
_, left_motor_handle=vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_leftMotor', vrep.simx_opmode_oneshot_wait)
_, right_motor_handle=vrep.simxGetObjectHandle(clientID, 'Pioneer_p3dx_rightMotor', vrep.simx_opmode_oneshot_wait)
 
#Guardar la referencia de la camara
_, camhandle = vrep.simxGetObjectHandle(clientID, 'Vision_sensor', vrep.simx_opmode_oneshot_wait)
 
#acceder a los datos del laser
_, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)


velocidad = 0.35 #Variable para la velocidad de los motores
 
#Iniciar la camara y esperar un segundo para llenar el buffer
_, resolution, image = vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_streaming)
time.sleep(1)
 
plt.axis('equal')
plt.axis([0, 4, -2, 2])    
nombre = ""
nombre = input("Introzuca el nombre de los ficheros: ")

while len(nombre) == 0:
    nombre = input("Se paso un nobmre no valido. Vuelva a intentarlo: ")
    
# mostramos el directorio de trabajo y vemos si existe el dir para salvar los datos
print("Directorio de trabajo es: ", os.getcwd())

directorio = ""
directorio = input("Introzuca el nombre del directorio: ")

while len(nombre) == 0:
    nombre = input("Se paso un nobmre no valido. Vuelva a intentarlo: ")
    
listaDir=sorted(glob.glob(directorio+'*'))

nuevoDir=directorio+str(len(listaDir))

if (os.path.isdir(nuevoDir)):
    sys.exit("Error: ya existe el directorio "+ nuevoDir)
else:
    os.mkdir(nuevoDir)
    os.chdir(nuevoDir)
    print("Cambiando el directorio de trabajo: ", os.getcwd())

#Creamos el fichero JSON para guardar los datos del laser
#usamos diccionarios
segundos=10
maxIter=50
iteracion=0

cabecera={"TiempoSleep":segundos,
          "MaxIteraciones":maxIter}

ficheroLaser=open(nombre+".json", "w")

ficheroLaser.write(json.dumps(cabecera)+'\n')


seguir=True
 
while(iteracion<maxIter and seguir):
    puntosx=[] #listas para recibir las coordenadas x, y z de los puntos detectados por el laser
    puntosy=[]
    puntosz=[]
    returnCode, signalValue = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_buffer) 
    time.sleep(segundos) #esperamos un tiempo para que el ciclo de lectura de datos no sea muy rápido
    datosLaser=vrep.simxUnpackFloats(signalValue)
    for indice in range(0,len(datosLaser),3):
        puntosx.append(datosLaser[indice+1])
        puntosy.append(datosLaser[indice+2])
        puntosz.append(datosLaser[indice])
    
    print("Iteración: ", iteracion)        
    plt.clf()    
    plt.plot(puntosx, puntosy, 'r.')
    plt.show()
    
    #Guardamos los puntosx, puntosy en el fichero JSON
    lectura={"Iteracion":iteracion, "PuntosX":puntosx, "PuntosY":puntosy}
    #ficheroLaser.write('{}\n'.format(json.dumps(lectura)))
    ficheroLaser.write(json.dumps(lectura)+'\n')
    
    
    
    #Guardar frame de la camara, rotarlo y convertirlo a BGR
    _, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
    img = np.array(image, dtype = np.uint8)
    img.resize([resolution[0], resolution[1], 3])
    img = np.rot90(img,2)
    img = np.fliplr(img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
 
     
    #Convertir img a hsv y detectar colores
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    verde_bajos = np.array([49,50,50], dtype=np.uint8)
    verde_altos = np.array([80, 255, 255], dtype=np.uint8)
    mask = cv2.inRange(hsv, verde_bajos, verde_altos) #Crear mascara
 
    #Limpiar mascara y buscar centro del objeto verde
    moments = cv2.moments(mask)
    area = moments['m00']
    if(area > 200):
        x = int(moments['m10']/moments['m00'])
        y = int(moments['m01']/moments['m00'])
        cv2.rectangle(img, (x, y), (x+2, y+2),(0,0,255), 2)
        #Descomentar para printear la posicion del centro
        #print(x,y)
 
        #Si el centro del objeto esta en la parte central de la pantalla (aprox.), detener motores
        if abs(x-256/2) < 15:
            vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,0,vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,0,vrep.simx_opmode_streaming)
 
        #Si no, girar los motores hacia la derecha o la izquierda
        elif x > 256/2:
            vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,velocidad,vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,-velocidad,vrep.simx_opmode_streaming)
        elif x < 256/2:
            vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,-velocidad,vrep.simx_opmode_streaming)
            vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,velocidad,vrep.simx_opmode_streaming)
 
 
    #Mostrar frame y salir con "ESC"
    cv2.imshow('Image', img)
    cv2.imshow('Mask', mask)
    
    if iteracion == 0:
        cv2.imwrite(nombre+str(iteracion + 1)+'.jpg', img)
        
        
    tecla = cv2.waitKey(5) & 0xFF
    if tecla == 27:
        seguir=False
    
    iteracion=iteracion+1
   
   
    


    
    
    


#detememos los motores
vrep.simxSetJointTargetVelocity(clientID, left_motor_handle,0,vrep.simx_opmode_streaming)
vrep.simxSetJointTargetVelocity(clientID, right_motor_handle,0,vrep.simx_opmode_streaming)
    
time.sleep(1)

#detenemos la simulacion
vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)

#cerramos la conexion
vrep.simxFinish(clientID)

#cerramos las ventanas
cv2.destroyAllWindows()

finFichero={"Iteraciones totales":iteracion}
#ficheroLaser.write('{}\n'.format(json.dumps(finFichero)))
ficheroLaser.write(json.dumps(finFichero)+'\n')
ficheroLaser.close()

#salvo a disco la ultima imagen
cv2.imwrite(nombre+str(iteracion)+'.jpg', img)
 





'''
Se pueden ver más métodos en
http://www.coppeliarobotics.com/helpFiles/en/remoteApiFunctionsMatlab.htm

por ejemplo para ver las velocidades de los motores usar
 
velocidadIz=vrep.simxGetObjectVelocity(clientID, left_motor_handle,vrep.simx_opmode_oneshot_wait)
velocidadDe=vrep.simxGetObjectVelocity(clientID, right_motor_handle,vrep.simx_opmode_oneshot_wait)

print("Velocidad iz: ", velocidadIz, " Velocidad de:", velocidadDe)

orientacionRobot=vrep.simxGetObjectOrientation(clientID, robothandle, 0, vrep.simx_opmode_oneshot_wait)

 print(orientacionRobot)


'''



    
    
    