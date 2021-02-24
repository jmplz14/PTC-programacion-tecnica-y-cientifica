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
"""
    devuelve la dinstacia euclidea de dos puntos
    Parameters: 
        -punto1= primer punto 2d
        -punto2= segundo punto 2d
        
    Returns: 
        -distancia euclidea
        
""" 
def distanciaEuclidea(punto1,punto2): 
    return math.sqrt(pow((punto1[0]-punto2[0]),2) + pow((punto1[1]-punto2[1]),2))

"""
    devuelve el perimetro de un cluster
    Parameters: 
        -puntoX= cordenadas x
        -puntoY = cordeandas y
        -tam= numero del punto
    Returns: 
        -perimetro de un cluster
        
""" 
def obtenerPerimetro(puntosX,puntosY,tam):
    perimetro = 0
    anterior = np.array([puntosX[0],puntosY[0]])
    
    for i in range(1,tam):
        actual = np.array([puntosX[i],puntosY[i]])
        perimetro += np.linalg.norm((actual - anterior))
        anterior = np.copy(actual)
        
    return perimetro
"""
    devuelve la anchura de un cluster
    Parameters: 
        -puntoX= cordenadas x
        -puntoY = cordeandas y
        -tam= numero del punto
    Returns: 
        -anchura del cluster
        
""" 
def obtenerAnchura(puntosX,puntosY,tam):
    primero = np.array([puntosX[0],puntosY[0]])
    ultimo = np.array([puntosX[tam - 1],puntosY[tam - 1]])
    return np.linalg.norm(ultimo-primero)
"""
    devuelve la profundidad de un cluster calandola desde el punto mas alejado a los extremos
    Parameters: 
        -puntoX= cordenadas x
        -puntoY = cordeandas y
        -tam= numero del punto
        
    Returns: 
        -profundidad cluster
        
""" 
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

"""
    devuelve un array con las tres caractericticas de un clustear
    Parameters: 
        -puntoX= cordenadas x
        -puntoY = cordeandas y
        -tam= numero del punto
        
    Returns: 
        -[perimetro,profundidad,anchura]
        
""" 
def obtenerDatos(puntosX,puntosY,tam):
    anchura = obtenerAnchura(puntosX,puntosY,tam)
    perimetro = obtenerPerimetro(puntosX,puntosY,tam)
    profundidad = obtenerProfundidad(puntosX,puntosY,tam)
    
    return [perimetro,profundidad,anchura]

"""
    Crea los fichoeros .data y el csv con los datos de anchura profundiad 
    y perimetro
    Parameters: 
        -ficheros: nombre de los ficheros de los que leeremos los datos 
        -ficheroCsv: nombre del fichero csv que guardaremos
        -ficheroJson: nobre del fichero json para guardaran los datos
        -tipo: si es 0 o 1 (noPierna o pierna) sera un array que correspondea a los 
        ficheros paradados en el primer parametro
        
    Returns: 

        
""" 
def crearFicheros(ficheros,ficheroCsv,ficherosJson,tipo):
    #abreimos el fichero csv para escribir
    salidacsv = open(ficheroCsv, "w")
    
    #contamos el numero de ficheros que leermos para realizar un for que los lea
    numFich = len(ficheros)
    for i in range(0,numFich):
        
        numCluster = 0
        #abrimos el json para guardar los datos
        salidajson = open(ficherosJson[i], "w")
        #abremos el ficheor
        with open(ficheros[i]) as f:
            #leemos linea a linea y nos quedamos los que tengan puntosX
            for line in f:  
                datos = json.loads(line)
                if 'puntosX' in datos:
                    #obtenemos los puntos
                    puntosX = datos["puntosX"] 
                    puntosY = datos["puntosY"]
                    tam = datos["numero_puntos"]

                    #obtenemos los valores para cada caracteristica
                    valores = obtenerDatos(puntosX,puntosY,tam)
                    
                    #se escribe tanto en el json como en el csv
                    dicc = {"numero_cluester":numCluster, "perimetro":valores[0], "profundidad":valores[1], "anchura":valores[2], "esPierna":tipo[i]}
                    
                    #guardamos en el csv y el json
                    salidacsv.write("""{}, {}, {}, {}\n""".format(valores[0],valores[1],valores[2],tipo[i])) 
                    salidajson.write(json.dumps(dicc)+'\n')
                    
                    #salidajson.write("{")
                    #salidajson.write(""""numero_cluester":{}, "perimetro":{}, "profundidad":{}, "anchura":{} "esPierna":{} """.format(numCluster,valores[0],valores[1],valores[2],tipo[i]))
                    #salidajson.write("}\n")
                    numCluster += 1
                    
        salidajson.close()
          
                
    
    salidacsv.close()  
    
    
if __name__ == "__main__":
    ficheros = ["clustersPiernas.json","clustersNoPiernas.json"]
    ficherosJson = ["carcteristicasPiernas.dat","carcteristicasNoPiernas.dat"]
    tipos = [1,0]
    
    crearFicheros(ficheros,"piernasDataset.csv",ficherosJson,tipos)
    