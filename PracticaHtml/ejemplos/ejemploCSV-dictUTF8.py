# -*- coding: utf-8 -*-
"""

@author: Eugenio
Ejemplo de operaciones con ficheros .csv y diccionarios
En este ejemplo el separador es el ;

Leemos el fichero poblacionPrueba.csv como un fichero de texto
para quitar la información que no interesa y generar un nuevo
poblacionPruebaFinal.csv con los datos de provincias y población en columnas

Aviso: puede haber problemas con la codificación según usemos windows o linux
por tanto en este ejemplo, leemos el fichero inicial en codificación windows
pero al escribir lo pasamos a utf8 para usar siempre utf8 como codificación de
los ficheros.


"""
import csv



#primero limpiar el archivo para quitar los datos no útiles
#dejar cabecera y datos
#el valor de codificacion es necesario en linux windows-1250, mejor ISO-8859-1

ficheroInicial=open("poblacionPrueba.csv","r", encoding="ISO-8859-1")


cadenaPob=ficheroInicial.read()

ficheroInicial.close()

print(cadenaPob)
print("aaa")
primero=cadenaPob.find("Total")
ultimo=cadenaPob.find("Notas")

cadenaFinal=cadenaPob[primero:ultimo]

#print(cadenaFinal)

cabecera="Provincia;H2017;H2016;H2015;M2017;M2016;M2015"

ficheroFinal=open("poblacionPruebaFinal.csv", "w",encoding="utf8")

ficheroFinal.write(cabecera+'\n'+cadenaFinal)

ficheroFinal.close()

# Leer el archivo 'poblacionPruebaFinal.csv' con reader() y 
# mostrar todos los registros, uno a uno:
""""print("Primer caso: se muestra cada linea como una lista de valores")
with open('poblacionPruebaFinal.csv', encoding="utf8") as csvarchivo:
    entrada = csv.reader(csvarchivo, delimiter=';')
    for reg in entrada:
        print(reg)  # Cada línea se muestra como una lista de valores"""
       
# en este segundo caso se lee como una serie de diccionarios
print("Segundo caso: se muestra cada linea como un diccionario")
with open('../poblacion/poblacionLimpiada.csv', encoding="utf8") as csvarchivo:
    poblacionDict = csv.DictReader(csvarchivo, delimiter=';')     
    for regD in poblacionDict:
        print(regD)
        
      


  
 
