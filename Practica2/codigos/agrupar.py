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
MAXIMO = 25
MINIMO = 3
DISTANCIA = 0.03
def buscarClusters(minimo,maximo,maxDistancia,puntosX,puntosY):
    cluster = list()
    tam = len(puntosX)
    anterior = [puntosX[0],puntosY[0]]
    inicioCluster = 0
    #print(tam)
    for i in range(1,tam):
        actual = [puntosX[i],puntosY[i]]
        distancia = math.sqrt(pow((actual[0]-anterior[0]),2) + pow((actual[1]-anterior[1]),2))
        #print(i,":",distancia)
        if distancia > maxDistancia:
            numPuntos = (i - inicioCluster)
            if numPuntos >= minimo and numPuntos <= maximo:
                cluster.append([inicioCluster,i-1])
            inicioCluster = i
        
        anterior = actual
    #print(inicioCluster,":",tam)
    if inicioCluster != tam - 1:
        numPuntos = (tam - 1  - inicioCluster)
        if numPuntos >= minimo and numPuntos <= maximo:
                cluster.append([inicioCluster,tam-1])
    
    
    return cluster
   
def crearJson(directorio,nombre):
    numCluster = 0
    #clusters = list()
    listaDir=sorted(glob.glob(directorio+'*'))
    salida = open(nombre, "w")
    for dirDatos in listaDir:
        fichero = glob.glob(dirDatos+'/*.json')
        print(fichero)
             
        if len(fichero) == 1:
            with open(fichero[0]) as f:
                for line in f:
                    datos = json.loads(line)
                    if 'PuntosX' in datos:
                        puntosX = datos["PuntosX"] 
                        puntosY = datos["PuntosY"]
                        cluster = buscarClusters(4,25,0.05,puntosX,puntosY)
                        for i in cluster:
                            numPuntos = i[1]-i[0] + 1
                            x = puntosX[i[0]:i[1] + 1]
                            y = puntosY[i[0]:i[1]+1]
                            #dicc = {"numero_cluster": numCluster, "numero_puntos": numPuntos , "puntosX": x, "puntosY": y}
                            #print(dicc)
                            salida.write("{")
                            salida.write(""""numero_cluster":{}, "numero_puntos":{}, "puntosX":{}, "puntosY":{}""".format(numCluster,numPuntos,x,y))
                            salida.write("}\n")
                            #salida.write(str(dicc))
                            numCluster += 1;
                    
            
    salida.close()
        
if __name__ == "__main__":
    crearJson("nuevoPositivo","clustersPiernas.json")
    crearJson("negativo","clustersNoPiernas.json")
    
    
        
        
        
            

        
    
    
