# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 14:29:03 2019

@author: Eugenio

Ejemplo para leer los valores de las tablas de HTML
usando beautiful soup 4
si no está instalado instalar con 
pip3 install bs4


"""

from bs4 import BeautifulSoup




#leemos el fichero de Comunidades
#el valor de codificacion es necesario en linux
        
comunidadesFich=open('comunidadesAutonomas.htm', 'r', encoding="ISO-8859-1")


comString=comunidadesFich.read()

soup = BeautifulSoup(comString, 'html.parser')

celdas=soup.find_all('td')

print(celdas)

lista=[]

for celda in celdas:
    lista.append(celda.get_text())

print(lista)

