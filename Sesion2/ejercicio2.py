#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:49:33 2019

@author: jose
"""
import math
num_valores = 3
x1 = float(input("Introduzca el x1: "))
x2 = float(input("Introduzca el x2: "))
x3 = float(input("Introduzca el x3: "))

media = (x1+x2+x3)/num_valores
sumatorita = (x1-media)**2 + (x2-media)**2 + (x3-media)**2
desviacion_tipica = math.sqrt(sumatorita/num_valores)

print("La desviacion tipica es ", desviacion_tipica)