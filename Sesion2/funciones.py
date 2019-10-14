#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 11:51:23 2019

@author: jose
"""

def funcion1(): 
    print("Modulo funciones. Función 1")
        
def funcion2(): 
    print("Modulo funciones. Función 2")
    
if __name__== "__main__":
    print("Modulo funciones es llamdo como fichero principal")
    funcion1()
    funcion2()
    
if __name__== "funciones":
    print("Modulo funciones esta siendo importado")
    funcion1()
    funcion2()