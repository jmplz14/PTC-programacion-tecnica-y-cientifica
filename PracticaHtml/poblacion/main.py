#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:56:53 2019

@author: jose
"""

import numpy as np
import locale
import math
from bs4 import BeautifulSoup


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
        
        
"""Generado apartir de R2"""
def diccComunidadesProvinciasHtml():
    numColumnas = 4
    comunidadesFich = open('comunidadesAutonomas.htm', 'r', encoding="ISO-8859-1")
    provinciasFich = open('comunidadAutonoma-Provincia.htm', 'r', encoding="ISO-8859-1")
    
    comString = comunidadesFich.read()
    provString = provinciasFich.read()
    
    
    soup = BeautifulSoup(comString, 'html.parser')
    valores = soup.find_all('td')
    
    diccNombresComunidad = {}
    diccProvinciasComunidad = {}
    
    for i in range(0,len(valores)//2):
        pos = i * 2
        
        codigo = valores[pos].get_text()
        codigo = codigo[:-1]
        nombre = valores[pos+1].get_text()
        
        diccNombresComunidad.update({codigo: nombre})
        
        diccProvinciasComunidad.update({codigo: {}})
    

    
    soup = BeautifulSoup(provString, 'html.parser')
    valores = soup.find_all('td')
    
    #ciudadesAutonomas = valores[50 * numColumnas + 3:]
    for i in range(3):
        valores.pop(50 * numColumnas)
        
    #valores = valores[:50 * numColumnas]
    
    
    #print(valores[50 * 4])
    
    for i in range(0,len(valores)//4):
        pos = i * 4
        codigoComunidad = valores[pos].get_text()
        codigoComunidad = codigoComunidad.replace(" ","")
        codigoProvincia = valores[pos+2].get_text()
        codigoProvincia = codigoProvincia.replace(" ","")
        nombreProvincia = valores[pos+3].get_text()
        #print(i)
        valoresComunidad = diccProvinciasComunidad[codigoComunidad]
        #print(valoresComunidad)
        valoresComunidad.update({codigoProvincia:nombreProvincia})
        #print(valoresComunidad)
        
        diccProvinciasComunidad.update({codigoComunidad: valoresComunidad} )
        
    #print(diccProvinciasComunidad)
  
    return diccNombresComunidad, diccProvinciasComunidad

def sumarArrayStringYNumpi(strings,numeros):
    stringNumerico = np.array(strings)
    stringNumerico = stringNumerico.astype(np.float)
    return numeros + stringNumerico
          
def generarDiccComunidades(diccDatos,diccProvinciasComunidad):
    diccDatosComunidades = {}
    
    for codComunidad in diccProvinciasComunidad:
        
        
        datosTotales = {"Totales":np.zeros(8),"Hombres":np.zeros(8),"Mujeres":np.zeros(8),}
        for codProvincia in diccProvinciasComunidad[codComunidad]:
            datosProvincia = diccDatos[codProvincia]
            
            suma = sumarArrayStringYNumpi(datosProvincia["Totales"],datosTotales["Totales"])
            datosTotales["Totales"] = suma
            
            suma = sumarArrayStringYNumpi(datosProvincia["Hombres"],datosTotales["Hombres"])
            datosTotales["Hombres"] = suma
            
            suma = sumarArrayStringYNumpi(datosProvincia["Mujeres"],datosTotales["Mujeres"])
            datosTotales["Mujeres"] = suma
            
        
        diccDatosComunidades.update({codComunidad: datosTotales})
        
    return diccDatosComunidades
            
            
            
            
def obtenerStringCsvNumpy(valores):
    stringCsv = ""
    for valor in valores:
        stringCsv += "{};".format(str(valor))
    return stringCsv

            
     
def R2(diccDatos,diccNombresComunidades,diccProvinciasComunidad):
    diccDatosComunidades = generarDiccComunidades(diccDatos,diccProvinciasComunidad)
    stringCsv = ";"
    cabecera = ["2017","2016","2015","2014","2013","2012","2011"]
    for i in range(3):
        for año in cabecera:
            stringCsv += "{};".format(año)
            
    for codComunidad in diccDatosComunidades:
        stringCsv += "\n"
        stringCsv += "{} {};".format(codComunidad, diccNombresComunidades[codComunidad])
        
        valores = diccDatosComunidades[codComunidad]
        stringCsv += obtenerStringCsvNumpy(valores["Totales"])
        stringCsv += obtenerStringCsvNumpy(valores["Hombres"])
        stringCsv += obtenerStringCsvNumpy(valores["Mujeres"])
        
    print(stringCsv)
        
            
        
    
    #diccProvinciasComunidades = diccProvinciasComunidadesHtml(diccNombresComunidades)
        

def main():
    diccDatos, diccNombres = cargarDiccionarioCsv()
    #R1(diccDatos, diccNombres, 2017)
    
    diccNombresComunidades, diccProvinciasComunidad, = diccComunidadesProvinciasHtml()
    R2(diccDatos,diccNombresComunidades,diccProvinciasComunidad)
    

    
    
    
    
  
if __name__== "__main__":
    main()
    