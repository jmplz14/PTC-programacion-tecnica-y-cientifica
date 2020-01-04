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
import agrupar
import caracteristicas

import pandas as pd
from sklearn.model_selection import train_test_split 
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.preprocessing import MinMaxScaler
from warnings import simplefilter
from sklearn.preprocessing import PolynomialFeatures
from sklearn import preprocessing as pp

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



#Creamos el fichero JSON para guardar los datos del laser
#usamos diccionarios
segundos=1


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
         

    
#Guardamos los puntosx, puntosy en el fichero JSON
#lectura={"PuntosX":puntosx, "PuntosY":puntosy}
cluster = agrupar.buscarClusters(4,25,0.05,puntosx,puntosy)
print(len(cluster))
print(cluster)





simplefilter(action='ignore', category=FutureWarning)
simplefilter(action='ignore', category=DeprecationWarning)

scaler = MinMaxScaler()


cabecera = ["perimetro","profundiad","anchura","clase"]
datos = pd.read_csv("piernasDataset.csv", names=cabecera) 
#datos[cabecera] = scaler.fit_transform(datos[cabecera])

X = datos.drop('clase', axis=1)  
"""print(X)
poly = PolynomialFeatures(degree=3, interaction_only=True)
poly = pp.PolynomialFeatures(2)
output_nparray = poly.fit_transform(X)
target_feature_names = ['x'.join(['{}^{}'.format(pair[0],pair[1]) for pair in tuple if pair[1]!=0]) for tuple in [zip(datos.columns,p) for p in poly.powers_]]
output_df = pd.DataFrame(output_nparray, columns = target_feature_names)
X=output_df
X = output_df"""

y = datos['clase'] 

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=8)

print("Clasificación con kernek de base radial con C=1 y gamma=auto")

svcRBF = SVC(kernel='rbf', gamma=20, C=1)
svcRBF.fit(X_train, y_train)


# Con el clasificador obtenido hacemos la predicción sobre el conjunto de test incial

y_pred = svcRBF.predict(X_test)

acc_test=accuracy_score(y_test, y_pred)

print("Acc_test RBF: (TP+TN)/(T+P)  %0.4f" % acc_test)

print("Matriz de confusión Filas: verdad Columnas: predicción")
'''
 Cij observaciones que son de clase i pero que se predicen a la clase j.
 La suma por filas son los ejemplos reales que hay de cada clase=soporte.
( TN	FP 
  FN	TP )
'''

print(confusion_matrix(y_test, y_pred))

'''
La precisión mide la capacidad del clasificador en no etiquetar como positivo un ejemplo que es negativo.
El recall mide la capacidad del clasificador para encontrar todos los ejemplos positivos.
'''

print("Precision= TP / (TP + FP), Recall= TP / (TP + FN)")
print("f1-score es la media entre precisión y recall")
print(classification_report(y_test, y_pred))

#Para asegurarnos de que el resultado no depende del conjunto de test elegido
#tenemos que realizar validación cruzada

svcRBF2 = SVC(kernel='rbf', gamma='auto')

scores = cross_val_score(svcRBF2, X, y, cv=5)

# exactitud media con intervalo de confianza del 95%
print("Accuracy 5-cross validation: %0.4f (+/- %0.4f)" % (scores.mean(), scores.std() * 2))
    
plt.clf() 

for i in cluster:
    numPuntos = i[1]-i[0] + 1
    x = puntosx[i[0]:i[1] + 1]
    y = puntosy[i[0]:i[1]+1]
    valores = caracteristicas.obtenerDatos(x,y,numPuntos)
    print(svcRBF.predict([valores]))
    print(len(x))
    if svcRBF.predict([valores]) == 1.:
        plt.plot(x, y, 'r.')
    else:
           
        plt.plot(x, y, 'b.')

plt.show()
    
#Guardar frame de la camara, rotarlo y convertirlo a BGR
_, resolution, image=vrep.simxGetVisionSensorImage(clientID, camhandle, 0, vrep.simx_opmode_buffer)
img = np.array(image, dtype = np.uint8)
img.resize([resolution[0], resolution[1], 3])
img = np.rot90(img,2)
img = np.fliplr(img)
img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
 
     
   


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



    
    