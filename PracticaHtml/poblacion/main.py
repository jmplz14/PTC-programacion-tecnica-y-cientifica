#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:56:53 2019

@author: jose
"""

import numpy as np
import locale
import math


locale.setlocale(locale.LC_ALL,'')

ficheroCsv = "poblacionProvinciasHM2010-17.csv"

def puntosDecimalesFloat(numero):
    return locale.format_string('%.2f', numero, grouping=True)
    
def puntosDecimalesInt(numero):
    return locale.format_string('%d', numero, grouping=True)

def redondear(numero,decimales):
    
    num_decimales = math.pow(10,decimales)
    if decimales > 0:
        numero=numero * num_decimales 
    numero=numero + 0.5
    numero=(int)(numero) # también se puede usar floor(numero)
    if decimales > 0:
        numero=numero / num_decimales

    return numero


def cargarDiccionarioCsv():
    
    ficheroInicial=open("poblacionProvinciasHM2010-17.csv","r", encoding="ISO-8859-1")
    cadenaPob=ficheroInicial.read()
    
    ficheroInicial.close()
    
    primero=cadenaPob.find("Total Nacional;")
    ultimo=cadenaPob.find("Notas")
    
    cadenaFinal=cadenaPob[primero:ultimo-1]
    i = 0
    
    for line in cadenaFinal.splitlines():
        arrayDatos = line[:-1].split(";")
        if i == 0:
            diccionarioDatos = {arrayDatos[0]: {"Totales": arrayDatos[1:9], "Hombres": arrayDatos[9:17], "Mujeres": arrayDatos[17:]}}
            
        else:  
            codigoNombre = arrayDatos[0].split(" ",1)
            
            if i == 1:
                diccionarioNombres = {codigoNombre[0]: codigoNombre[1]}
            else:
                diccionarioNombres.update({codigoNombre[0]: codigoNombre[1]})
                
            diccionarioDatos.update({codigoNombre[0]: {"Totales": arrayDatos[1:9], "Hombres": arrayDatos[9:17], "Mujeres": arrayDatos[17:]}})
            
        
        i += 1
    
    return diccionarioDatos,diccionarioNombres
        #print(diccionarioNombre)
            #diccionario.update{"Codigo": }

    
def R1(diccDatos, diccNombres, añoInicio):
    diccVarRelativa, diccVarAbsoluta = obtenerDiccVariacion(diccDatos,"Totales")
    
    f = open('variacionProvincias2017-11.html','w', encoding="utf8" )
    
    pagina = """<!DOCTYPE html><html>
    <head><title>Apartado 1</title>
    <link rel="stylesheet" href="estilo.css">
    <meta charset="utf8"></head>
    <body><h1>Tabla ejercicio 1: variacion por proviencias</h1>
    <table>"""
    
    cabecera = ["2017","2016","2015","2014","2013","2012","2011"]
    
    cabeceraHtml = """\n\t<tr>\n\t\t<th> </th>"""
    for i in range(2):
        for i in cabecera:
            cabeceraHtml += """\t<th>{}</th>""".format(i)
    
    cabeceraHtml += "\n\t</tr>\n"

    pagina += cabeceraHtml

   
    cuerpoTabla = """<tr>
    <th> </th> <th colspan="{}" >Absoluta</th> <th colspan="{}">Relativa</th> 
    </tr>\n""".format(len(cabecera),len(cabecera))
    for codigo in diccDatos:
        if codigo in diccNombres:
            nombre = diccNombres[codigo];
        else:
            nombre = ""
        columnaTabla = "\t<tr>\n\t\t <td>{} {}</td>".format(codigo,nombre)
        absoluta = diccVarAbsoluta[codigo]
        relativa = diccVarRelativa[codigo]
        for i in absoluta:
            columnaTabla += "<td>{}</td>".format(puntosDecimalesInt(i))
        for i in relativa:
            columnaTabla += "<td>{}</td>".format(puntosDecimalesFloat(i))
        
        columnaTabla += "\n\t</tr>\n" 
        
        cuerpoTabla += columnaTabla

    pagina += cuerpoTabla
    
    pagina += "</table>\n</body>\n</html>"
    
    
    f.write(pagina)
    f.close
    
    #print(pagina)
 
def obtenerDiccVariacion(diccDatos,tipo):
    decimales = 100
    diccDatosVarAbsoluta = {}
    diccDatosVarRelativa = {}
    
    for dato in diccDatos: 
        datosActuales = diccDatos[dato];
        datosActuales = datosActuales[tipo]
        
        numElementos = len(datosActuales) - 1
        
        datosVarAbsoluta = np.empty(numElementos)
        datosVarRelativa = np.empty(numElementos)
        
        for i in range(numElementos):
            valorAbsoluta = int(float(datosActuales[i]) - float(datosActuales[i+1]))
            valorAbsoluta = redondear(valorAbsoluta,decimales)
            valorRelativa = (valorAbsoluta / float(datosActuales[i+1])) * 100
            valorRelativa = redondear(valorRelativa,decimales)
            datosVarAbsoluta[i] = valorAbsoluta
            datosVarRelativa[i] = valorRelativa
            
            
        diccDatosVarAbsoluta.update({dato: datosVarAbsoluta})
        diccDatosVarRelativa.update({dato: datosVarRelativa}) 
        
    return diccDatosVarRelativa, diccDatosVarAbsoluta
        
        

            
     
    
        

def main():
    diccDatos, diccNombres = cargarDiccionarioCsv()
    R1(diccDatos, diccNombres, 2017)
    

    
    
    
    
  
if __name__== "__main__":
    main()
    