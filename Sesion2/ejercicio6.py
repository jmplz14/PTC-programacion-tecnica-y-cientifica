#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 11:05:27 2019

@author: jose
"""
strin = "Hola"
contrario = ""
for i in range(1,len(strin) + 1):
    contrario = contrario + strin[-i]
print(contrario)
num_valores = 3
n1 = float(input("Introduzca el numero 1: "))
n2 = float(input("Introduzca el numero 2: "))
n3 = float(input("Introduzca el nuemero 3: "))
mayor = n3
menor = n3

if n1 > n2 and n1 > n3:
    mayor = n1
elif n2 > n3:
    mayor = n2

if n1 < n2 and n1 < n3:
    menor = n1
elif n2 < n3:
    menor = n2
    
print("El mayor es {} y el menor {} ".format(mayor,menor))

for i in range(3,1):
    print(i)