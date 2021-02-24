#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan  1 18:03:42 2020

@author: jose
"""
import json 
import numpy as np
import math
import glob
"""masimo = 25
minimo = 3
distancia = 0.03"""

"""
    Procesa los puntos x e y para obtener el numero de puntos que tiene el cluster por 
    el que empieza el array
    Parameters: 
        -maximo= numero maximo de puntos
        -maxDistnacia= distancia maxima entre putnos
        -puntosx= putnos x del cluster
        -puntosy= puntos y del cluster
        
    Returns: 
        Devuelve el numero puntos que contiene le cluster
        
"""
def procesarClusters(maximo,maxDistancia,puntosX,puntosY):
    tam = len(puntosX)
    parada = False
    #guardamos el punto y ponemos a 1 para el siguiente
    anterior = [puntosX[0],puntosY[0]]
    i = 1
    numPuntosAñadidos = 0
    
    #recorremos los array x e y para obtener puntos
    while parada == False and i < tam and i < maximo :
        #obtenemos el punto actual
        actual = [puntosX[i],puntosY[i]]
        #calculamos la distancia entre el actualy el anterior
        distancia = math.sqrt(pow((actual[0]-anterior[0]),2) + pow((actual[1]-anterior[1]),2))
        #si es una distancia valida contiuna y suma los puntos y la i si no marca la parada
        if distancia <= maxDistancia:
            numPuntosAñadidos += 1
            i += 1
        else:
            parada = True
        #guardamos el actual para la siguiente pasada
        anterior = actual
    
    return numPuntosAñadidos
            
"""
    obtiene los indices de inicio y final de todos los cluster de los puntos x e y
    Parameters: 
        -minimo= numeros minimos que pude tiener un cluster
        -maximo= numero maximo de puntos
        -maxDistnacia= distancia maxima entre putnos
        -puntosx= putnos x del cluster
        -puntosy= puntos y del cluster
        
    Returns: 
        -cluster array con los indices de inicio y final de todos los cluster que tenemos
        
"""   
def buscarClusters(minimo,maximo,maxDistancia,puntosX,puntosY):
    cluster = list()
    tam = len(puntosX)

    i = 0
    #recorremos x e y
    while i < tam:
        #pasamos los vecctores de x e y desde el indice i para obtener los cluster que tiene
        numPuntosCluster = procesarClusters(maximo,maxDistancia,puntosX[i:],puntosY[i:])
        #el numero de fin de cluster que nos devuelve es menor que el minimo - 1 el cluster
        #es demasiado pequeño y no se guarda
        if numPuntosCluster >= minimo - 1:
            cluster.append([i,i+numPuntosCluster])
            
        #avanzamos el indice
        i += numPuntosCluster + 1 
  
    return cluster

"""
   guarda los datos en el 
    Parameters: 
        -directorio= directorio en el que guardamos los ficheros
        -nombre= fichero donde tendremos los datos de x e y
        
    Returns: 
        -cluster array con los indices de inicio y final de todos los cluster que tenemos
        
"""    
def crearJson(directorio,nombre):
    numCluster = 0
    #clusters = list()
    #obtenemos los directiros
    listaDir=sorted(glob.glob(directorio+'*'))
    
    #creamos el fichero de salida
    salida = open(nombre, "w")
    #recorremos todos los directorios
    for dirDatos in listaDir:
        #obtenemos el fichero json del directoroio
        fichero = glob.glob(dirDatos+'/*.json')
        print(fichero)
        
        #miramos que solo tengamos uno
        if len(fichero) == 1:
            #obtenemos los putnos de l json
            with open(fichero[0]) as f:
                for line in f:
                    datos = json.loads(line)
                    if 'PuntosX' in datos:
                        puntosX = datos["PuntosX"] 
                        puntosY = datos["PuntosY"]
                        #obtenemos los clusters
                        cluster = buscarClusters(4,20,0.05,puntosX,puntosY)
                        #recorremos los clusters
                        for i in cluster:
                            numPuntos = i[1]-i[0] + 1
                            x = puntosX[i[0]:i[1] + 1]
                            y = puntosY[i[0]:i[1]+1]
                            #escribimos los datos en el json
                            dicc = {"numero_cluster": numCluster, "numero_puntos": numPuntos , "puntosX": x, "puntosY": y}
                            salida.write(json.dumps(dicc)+'\n')
                            #salida.write("{")
                            #salida.write(""""numero_cluster":{}, "numero_puntos":{}, "puntosX":{}, "puntosY":{}""".format(numCluster,numPuntos,x,y))
                            #salida.write("}\n")
                            #salida.write(str(dicc))"""
                            numCluster += 1;
                    
    print("Cluster generados: ", numCluster)      
    #cerramos el fichero    
    salida.close()
        
if __name__ == "__main__":
    crearJson("positivo","clustersPiernas.json")
    crearJson("negativo","clustersNoPiernas.json")
    
    
        
        
        
            

        
    
    
