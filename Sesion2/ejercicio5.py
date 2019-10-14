#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 11:21:10 2019

@author: jose
"""

def pedirMomento():
    horas = int(input("Introduzca las horas: "))
    minutos = int(input("Introduzca los minutos: "))
    segundos = int(input("Introduzca los segundos: "))
    
    return horas,minutos,segundos

def convertirASegundos(horas,minutos,segundos):
    total = segundos + minutos * 60 + horas * 3600
    return total

def formatearSegundos(total_seg):
    horas = int(total_seg / 3600)
    segundos = total_seg % 60
    minutos = int((total_seg - (horas * 3600) - segundos)/ 60)
    return horas, minutos, segundos

print("Introzuca el primer instante")
hora1, min1, seg1 = pedirMomento()
print("Introduzca el segundo instante")
hora2, min2, seg2 = pedirMomento()

instante1 = convertirASegundos(hora1,min1,seg1)
instante2 = convertirASegundos(hora2,min2,seg2)

hora_dif,min_dif,seg_dif = formatearSegundos(abs(instante1-instante2))

print("Pasaron {}:{}:{}".format(hora_dif,min_dif,seg_dif))