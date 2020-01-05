#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  2 14:17:04 2020

@author: jose
"""
import sys
import json
import math
import numpy as np
#actual, anterior
def distanciaEuclidea(punto1,punto2): 
    return math.sqrt(pow((punto1[0]-punto2[0]),2) + pow((punto1[1]-punto2[1]),2))

def obtenerPerimetro(puntosX,puntosY,tam):
    perimetro = 0
    anterior = np.array([puntosX[0],puntosY[0]])
    
    for i in range(1,tam):
        actual = np.array([puntosX[i],puntosY[i]])
        perimetro += np.linalg.norm((actual - anterior))
        anterior = np.copy(actual)
        
    return perimetro

def obtenerAnchura(puntosX,puntosY,tam):
    primero = np.array([puntosX[0],puntosY[0]])
    ultimo = np.array([puntosX[tam - 1],puntosY[tam - 1]])
    return np.linalg.norm(ultimo-primero)
def obtenerProfundidad(puntosX,puntosY,tam):
    p1 = np.array([puntosX[0],puntosY[0]])
    p2 = np.array([puntosX[tam - 1],puntosY[tam - 1]])
    profundidadMax = 0
    if tam > 2:
        profundidadMax = sys.float_info.max
        for i in range(1,tam-1):
            p3 = np.array([puntosX[i],puntosY[i]])
            profundidad = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
            if profundidad < profundidadMax:
                profundidadMax = profundidad
        
    return profundidad

def obtenerDatos(puntosX,puntosY,tam):
    anchura = obtenerAnchura(puntosX,puntosY,tam)
    perimetro = obtenerPerimetro(puntosX,puntosY,tam)
    profundidad = obtenerProfundidad(puntosX,puntosY,tam)
    
    return [perimetro,profundidad,anchura]
def crearFicheros(ficheros,ficheroCsv,ficherosJson,tipo):
    
    salidacsv = open(ficheroCsv, "w")
    numFich = len(ficheros)
    
    for i in range(0,numFich):
        numCluster = 0
        salidajson = open(ficherosJson[i], "w")
        with open(ficheros[i]) as f:
            for line in f:  
                datos = json.loads(line)
                if 'puntosX' in datos:
                    
                    puntosX = datos["puntosX"] 
                    puntosY = datos["puntosY"]
                    tam = datos["numero_puntos"]
                    #anchura = obtenerAnchura(puntosX,puntosY,tam)
                    #perimetro = obtenerPerimetro(puntosX,puntosY,tam)
                    #profundidad = obtenerProfundidad(puntosX,puntosY,tam)
                    valores = obtenerDatos(puntosX,puntosY,tam)
                    salidacsv.write("""{}, {}, {}, {}\n""".format(valores[0],valores[1],valores[2],tipo[i])) 
                    
                    salidajson.write("{")
                    salidajson.write(""""numero_cluester":{}, "perimetro":{}, "profundidad":{}, "anchura":{} "esPierna":{} """.format(numCluster,valores[0],valores[1],valores[2],tipo[i]))
                    salidajson.write("}\n")
                    numCluster += 1
                    
        salidajson.close()
                
                
    
    salidacsv.close()  
    
    
if __name__ == "__main__":
    ficheros = ["clustersPiernas.json","clustersNoPiernas.json"]
    ficherosJson = ["carcteristicasPiernas.dat","carcteristicasNoPiernas.dat"]
    tipos = [1,0]
    
    crearFicheros(ficheros,"piernasDataset.csv",ficherosJson,tipos)
    