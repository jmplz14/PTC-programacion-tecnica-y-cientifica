#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:56:02 2019

@author: jose
"""

horas = int(input("Introduzca las horas: "))
minutos = int(input("Introduzca los minutos: "))
segundos = int(input("Introduzca los segundos: "))

segundos_totales = segundos % 60

minutos_totales = minutos + int(segundos / 60)

horas_totales = int(minutos_totales / 60)  + horas

minutos_totales = minutos_totales % 60

print("Son ", horas_totales, " horas ", minutos_totales,  " minutos y ", segundos_totales, " segundos")
