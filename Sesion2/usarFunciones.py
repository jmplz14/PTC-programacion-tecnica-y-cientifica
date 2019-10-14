#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:54:51 2019

@author: jose
"""

import funciones as fc
from funciones import funcion1
print("Este programa usa las funciones del mundulo funciones")

fc.funcion1()
funcion1()
fc.funcion1()


numero1 = 0.1 + 0.1 + 0.1
numero2 = 0.3

if numero1 == numero2:
    print("Son iguales")
else:
    print("No son iguales")
    
if numero1 == 0.3:
    print("Son iguales")
else:
    print("No son iguales")
    