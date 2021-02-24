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
from collections import OrderedDict
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

"""
    devuelve el punto al qu epertenece el centroyde para un cluster
    Parameters: 
        -puntoX= cordenadas x de todos los puntos del cluster
        -puntoY = cordenadas y de todos los puntos del cluster

        
    Returns: 
        -centroide= un punto 2d 
        
""" 
def centeroidnp(x,y):
    valores = np.array([x,y])
    centroide = np.mean(valores, axis=1)
    return centroide


"""
    recorre todos los cluster obtienen el mas cercano a el acutal y si es de la misma
    clase y esta a menos distancia de la maxima, calcula el centroide entre ellos
    Parameters: 
        -centroides= punto que pertenece a los centroide de todos los clusters
        -clases= array que contiene la clase de cada uno de los centroides
        -dMax=0.7 distancia maxiama a la que consideramos que ya no son el mismo objeto
        y no tiene centroide

        
    Returns: 
        centroide_clusters= puntos 2d que corresponden al centroide entre dos clusters
        clases_centroide_clusters= clases de los cluster del que se obtuvieron los centroides
        
""" 
def calcular_punto_medio_centroides(centroides, clases,dMax = 0.7):    
    
    #mediante KDtre ordenamos para buscar a continacion por distnaica
    arbol = KDTree(np.array(centroides))
    #obtenemos los dos mas cercanos para cada centroide y nos quedamos el segundo
    #el primero es el mismo centroide
    pos_cercano = arbol.query(centroides, k=2, return_distance=False)[:, 1]
    emparejados = list()
    
    centroide_clusters = list()
    clases_centroide_clusters = list()
    
    #recorremos los centroides
    for i in range(0,len(centroides)):
        #obtenemos distancia entre el centroide y su mas cercano
        cercano = pos_cercano[i]
        distancia = caracteristicas.distanciaEuclidea(centroides[i],centroides[cercano])
        
        #si son de la misma clase no ha sido ya emparejado a otro y nno supera la disntacia maxima
        #caluclaremos el nuevo centroide
        if clases[i] == clases[cercano] and cercano not in emparejados and distancia<dMax:
            punto = centroides[i]
            #marcamos como ya emparejados
            emparejados.append(cercano)
            emparejados.append(i)
            #calculamos el centroide lo guardamos y se guarda la clase tambien
            medio = (punto+centroides[cercano]) / 2
            centroide_clusters.append(medio)
            clases_centroide_clusters.append(clases[cercano])
            
    return centroide_clusters,clases_centroide_clusters
"""
    Dibujamos todos los cluster en la grafica con su color segun el tipo de clase al 
    que pertenece
        -svcRBF modelo para predecir si es pie o no es pie
        -cluster= indices de los cluster que dibujaremos
        -puntosx = putnos x dados por el laser
        -puntosy = puntos y dados por el laser
    Returns:
        
""" 
def dibujarCluster(svcRBF,cluster,puntosx,puntosy):
    #iniciamos la grafica
    plt.clf() 
    plt.figure(figsize=(10,10))
    puntos = list()
    clases = list()
    
    #recorremos los clusters
    for i in cluster:
        #obtenemos los putnos de el cluster quedandonos el punto inicial  y el 
        #numero de putnos que contiene
        numPuntos = i[1]-i[0] + 1
        x = puntosx[i[0]:i[1] + 1]
        y = puntosy[i[0]:i[1]+1]
        
        #obtenemos la profundidad anchura y perimetro del cluster
        valores = caracteristicas.obtenerDatos(x,y,numPuntos)
        #obteenmos el centroide de este
        centro = centeroidnp(x,y)
        
        #guardamos el centroide para ser dspues dibujados
        puntos.append(centro)
        
        #predecimos si es pierna o no 
        clase = svcRBF.predict([valores])
        
        #guardamos la clase par asaber a continuacion de que clase es un centroide
        clases.append(clase)
        
        #dibujamos el clustar si es pierna en rojo y azul si no e spierna
        if clase == 1.:
            plt.plot(x, y, 'r.', label="Pierna")
        else:
            plt.plot(x, y, 'b.', label="No pierna")
            
    #obtenemos los centroides de los clustar que osno de la misma clase y a menor distancia de la maxima
    centroides, clases_centroides = calcular_punto_medio_centroides(puntos,clases) 
    
    #dibujamos los centroides
    for i in range(0,len(clases_centroides)):
        plt.plot(centroides[i][0],centroides[i][1],'g+', label="Centroide")
     
    #añadimos la legenda
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = OrderedDict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys())
    
    #dibuajmos la grafica
    plt.show()     
    
    
if __name__ == "__main__":
    clientID = capturar.realizarConexion()



        
     
    #acceder a los datos del laser
    _, datosLaserComp = vrep.simxGetStringSignal(clientID,'LaserData',vrep.simx_opmode_streaming)
    time.sleep(1)
    
    #capturar.iniciarGrafica()  
    
    
    
    #obtenemos los putnos del laser
    puntosx, puntosy = capturar.obtenerPuntosXY(clientID)
    #obtenemos los cluster 
    cluster = agrupar.buscarClusters(4,20,0.05,puntosx,puntosy)
    
    #cargamos nuestro modelo
    svcRBF = load("modelo.joblib")
    #dibuajmos los clusters en la grafica
    dibujarCluster(svcRBF,cluster,puntosx,puntosy)
    
    #paramos la simulacion
    capturar.detenerSimulacion(clientID)
        
    time.sleep(1)
    

    
    
    
        
        