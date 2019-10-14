#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 10:39:27 2019

@author: jose
"""

precio_bruto = float(input("Introduzca el precio bruto: "))
ganacia = float(input("Introduzca el porcentaje de ganancia: "))
iva = float(input("Introduzca el porcentaje de IVA: "))

precio_base = precio_bruto * (1 + ganacia / 100)

print("Precio base es de ", precio_base, "€")
print("Precio con IVA es de ", precio_base *(1 + iva / 100),"€")