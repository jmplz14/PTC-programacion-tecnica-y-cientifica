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
    anterior = [puntosX[0],puntosY[0]]
    
    for i in range(1,tam):
        actual = [puntosX[i],puntosY[i]]
        perimetro += distanciaEuclidea(actual,anterior)
        anterior = actual
        
    return perimetro

def obtenerAnchura(puntosX,puntosY,tam):
    primero = [puntosX[0],puntosY[0]]
    ultimo = [puntosX[tam - 1],puntosY[tam - 1]]
    return distanciaEuclidea(primero,ultimo)
def obtenerProfundidad(puntosX,puntosY,tam):
    p1 = np.array([puntosX[0],puntosY[0]])
    p2 = np.array([puntosX[tam - 1],puntosY[tam - 1]])
    profundiadMax = 0
    if tam > 2:
        profundiadMax = sys.float_info.max
        for i in range(1,tam-1):
            p3 = np.array([puntosX[i],puntosY[i]])
            profundiad = np.linalg.norm(np.cross(p2-p1, p1-p3))/np.linalg.norm(p2-p1)
            if profundiad < profundiadMax:
                profundiadMax = profundiad
        
    return profundiad



salidacsv = open("datos.csv", "w")
salidajson = open("salida.json", "w")
tipo = 0
with open('prueba.json') as f:
    for line in f:  
        datos = json.loads(line)
        if 'puntosX' in datos:
            
            puntosX = datos["puntosX"] 
            puntosY = datos["puntosY"]
            tam = datos["numero_puntos"]
            anchura = obtenerAnchura(puntosX,puntosY,tam)
            perimetro = obtenerPerimetro(puntosX,puntosY,tam)
            profundiad = obtenerProfundidad(puntosX,puntosY,tam)
            salidacsv.write("""{}, {}, {}, {}\n""".format(perimetro,profundiad,anchura,tipo)) 
            
            
                
            
            
            

salidacsv.close()  
salidajson.close()