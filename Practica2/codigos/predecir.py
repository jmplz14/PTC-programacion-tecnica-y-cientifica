# -*- coding: utf-8 -*-
"""
    Vrep y OpenCV en Python
    Codigo escrito por Glare
    www.robologs.net
    Modificado para practica PCT por Eugenio Aguirre
    Leemos datos de laser, los mostramos con matplot y los salvamos a un fichero JSON
    Importante: La escena tiene que estar ejecutándose en el simulador (Usar botón PLAY)
"""
from joblib import load
import vrep
import capturar
import cv2
import numpy as np
import time
import matplotlib.pyplot as plt
import agrupar
import caracteristicas
from sklearn.neighbors import KDTree


import pandas as pd


def centeroidnp(x,y):
    valores = np.array([x,y])
    centroide = np.mean(valores, axis=1)
    return centroide

def calcular_punto_medio_centroides(centroides, clases):    
 
    arbol = KDTree(np.array(centroides))
    pos_cercano = arbol.query(centroides, k=2, return_distance=False)[:, 1]
    emparejados = list()
    
    centroide_clusters = list()
    clases_centroide_clusters = list()
    
    for i in range(0,len(centroides)):
        
        cercano = pos_cercano[i]
        distancia = caracteristicas.distanciaEuclidea(centroides[i],centroides[cercano])
        
        if clases[i] == clases[cercano] and cercano not in emparejados and distancia<0.7:
            punto = centroides[i]
            emparejados.append(cercano)
            emparejados.append(i)
            medio = (punto+centroides[cercano]) / 2
            centroide_clusters.append(medio)
            clases_centroide_clusters.append(clases[cercano])
            
    return centroide_clusters,clases_centroide_clusters
            
def dibujarCluster(svcRBF,cluster):
    plt.clf() 
    plt.figure(figsize=(10,10))
    puntos = list()
    clases = list()
    for i in cluster:
        numPuntos = i[1]-i[0] + 1
        x = puntosx[i[0]:i[1] + 1]
        y = puntosy[i[0]:i[1]+1]
        valores = caracteristicas.obtenerDatos(x,y,numPuntos)
        centro = centeroidnp(x,y)
        
        puntos.append(centro)
        clase = svcRBF.predict([valores])
        clases.append(clase)
        if clase == 1.:
            plt.plot(x, y, 'r.')
        else:
            plt.plot(x, y, 'b.')
        
    centroides, clases_centroides = calcular_punto_medio_centroides(puntos,clases) 
    for i in range(0,len(clases_centroides)):
        if clases_centroides[i] == 1:
            plt.plot(centroides[i][0],centroides[i][1],'g+')
        else:
            plt.plot(centroides[i][0],centroides[i][1],'g+')
    
    plt.show()     
    
    
if __name__ == "__main__":
    clientID = capturar.realizarConexion()



        
     
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    time.sleep(1)
     
    capturar.iniciarGrafica()  
    
    
    
    #Creamos el fichero JSON para guardar los datos del laser
    #usamos diccionarios
    
    
    puntosx, puntosy = capturar.obtenerPuntosXY(clientID)
    
    cluster = agrupar.buscarClusters(4,20,0.05,puntosx,puntosy)
    
    
    cabecera = ["perimetro","profundiad","anchura","clase"]
    datos = pd.read_csv("piernasDataset.csv", names=cabecera) 

    svcRBF = load("modelo.joblib")
    dibujarCluster(svcRBF,cluster)
    
    
    capturar.detenerSimulacion(clientID)
        
    time.sleep(1)
    
    #detenemos la simulacion
    vrep.simxStopSimulation(clientID,vrep.simx_opmode_oneshot_wait)
    
    #cerramos la conexion
    vrep.simxFinish(clientID)
    
    #cerramos las ventanas
    cv2.destroyAllWindows()
    
    
    
    
        
        