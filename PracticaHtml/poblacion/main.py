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
from collections import Counter
import matplotlib.pyplot as plt
import os
locale.setlocale(locale.LC_ALL,'')

ficheroCsv = "poblacionProvinciasHM2010-17.csv"
añoInicio = 2017
añoFinal = 2010
carpetaDatos = "resultados/"


def puntosDecimalesFloat(numero):
    return locale.format_string('%.2f', numero, grouping=True)
    
def puntosDecimalesInt(numero):
    return locale.format_string('%d', numero, grouping=True)



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

def generarWebAbsolutaRelativa(diccDatos,diccNombres,tipos,titulo,fichero,imagen = None):
    
    numTipos = len(tipos)
    diccVarRelativa, diccVarAbsoluta = obtenerDiccVariacion(diccDatos,tipos)
    f = open(carpetaDatos + fichero,'w', encoding="utf8" )
    
    pagina = """<!DOCTYPE html><html>
    <head><title>{}</title>
    <link rel="stylesheet" href="../estilo.css">
    <meta charset="utf8"></head>
    <body>
    <table>""".format(titulo)
    
    cabecera = ["2017","2016","2015","2014","2013","2012","2011"]
    
    cabeceraHtml = """\n\t<tr>\n\t\t<th> </th>"""
    for i in range(numTipos * 2):
        for i in cabecera:
            cabeceraHtml += """\t<th>{}</th>""".format(i)
    
    cabeceraHtml += "\n\t</tr>\n"

    pagina += cabeceraHtml

   

    numAños = len(cabecera)
    if numTipos > 1:
        cabeceraTipos = """\n\t<tr>\n\t\t<th> </th>"""
        for i in tipos:
            cabeceraTipos += """\t<th colspan="{}" >{}</th>""".format(numAños * 2,i)
            
        cabeceraTipos += "\n\t</tr>\n"
        pagina += cabeceraTipos
    
    
    cuerpoTabla = """<tr>
    <th> </th> """ 
    
    for i in range(numTipos):
        cuerpoTabla +="""<th colspan="{0}" >Absoluta</th> <th colspan="{0}">Relativa</th>""".format(numAños)
        
    cuerpoTabla += "\n</tr>\n"
    
    

    for codigo in diccDatos:
        if codigo in diccNombres:
            nombre = diccNombres[codigo];
        else:
            nombre = ""
        columnaTabla = "\t<tr>\n\t\t <th>{} {}</th>".format(codigo,nombre)
        absoluta = diccVarAbsoluta[codigo]
        relativa = diccVarRelativa[codigo]
        
        for posTipo in range(numTipos):
            for i in range(numAños):
                pos = posTipo * numAños + i
                #print(pos)
                columnaTabla += "<td>{}</td>".format(puntosDecimalesInt(absoluta[pos]))
            for i in range(numAños):
                pos = posTipo * numAños + i
                columnaTabla += "<td>{}</td>".format(puntosDecimalesFloat(relativa[pos]))
                
        columnaTabla += "\n\t</tr>\n" 
            
        cuerpoTabla += columnaTabla

    pagina += cuerpoTabla
    
    if imagen != None:
        pagina += """</table>\n<img src="{}">\n""".format(imagen)
        pagina += "</body>\n</html>"
    else:
        pagina += "</table>\n</body>\n</html>"
    
    
    f.write(pagina)
    f.close
    
def R1(diccDatos, diccNombres):
    titulo = "Apartado 1"
    pagina = "variacionProvincias.html"
    tipos = ["Totales"]
    generarWebAbsolutaRelativa(diccDatos,diccNombres,tipos,titulo,pagina)
    
    
    
    #print(pagina)
 
def obtenerDiccVariacion(diccDatos,tipos):
    diccDatosVarAbsoluta = {}
    diccDatosVarRelativa = {}
    
    for tipo in tipos:
        for dato in diccDatos: 
            datosActuales = diccDatos[dato];
            datosActuales = datosActuales[tipo]
            
            numElementos = len(datosActuales) - 1
            
            datosVarAbsoluta = np.empty(numElementos)
            datosVarRelativa = np.empty(numElementos)
            
            for i in range(numElementos):
                valorAbsoluta = int(float(datosActuales[i]) - float(datosActuales[i+1]))
                valorRelativa = (valorAbsoluta / float(datosActuales[i+1])) * 100
                datosVarAbsoluta[i] = valorAbsoluta
                datosVarRelativa[i] = valorRelativa
                
            if dato in diccDatosVarAbsoluta.keys():
                valores = np.concatenate((diccDatosVarAbsoluta[dato] ,datosVarAbsoluta))
                diccDatosVarAbsoluta.update({dato: valores})
                #print(diccDatosVarRelativa[dato])
                #print(datosVarRelativa)
                valores = np.concatenate((diccDatosVarRelativa[dato] ,datosVarRelativa))
                
                diccDatosVarRelativa.update({dato: valores})
                #print(diccDatosVarRelativa[dato])
                
            else:
                diccDatosVarAbsoluta.update({dato: datosVarAbsoluta})
                diccDatosVarRelativa.update({dato: datosVarRelativa}) 
                
                
    return diccDatosVarRelativa, diccDatosVarAbsoluta
        
        
"""Generado apartir de R2"""
def diccComunidadesProvinciasHtml(ficheroComunidades):
    numColumnas = 4
    comunidadesFich = open(ficheroComunidades, 'r', encoding="ISO-8859-1")
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
        if codigoComunidad in diccProvinciasComunidad.keys():
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

            
def generarWebComunidades(diccNombresComunidades,diccDatosComunidades,nombreWeb,nombreImagen):
    f = open(carpetaDatos + nombreWeb,'w', encoding="utf8" )
    
    pagina = """<!DOCTYPE html><html>
    <head><title>Apartado 2 y 3</title>
    <link rel="stylesheet" href="../estilo.css">
    <meta charset="utf8"></head>
    <body>
    <table>"""
    
    cabecera = ["2017","2016","2015","2014","2013","2012","2011","2010"]
    
    cabeceraHtml = """\n\t<tr>\n\t\t<th> </th>"""
    for i in range(2):
        for i in cabecera:
            cabeceraHtml += """\t<th>{}</th>""".format(i)
    
    cabeceraHtml += "\n\t</tr>\n"

    pagina += cabeceraHtml

    cuerpoTabla = """<tr>
    <th> </th> <th colspan="{0}" >Hombres</th> <th colspan="{0}">Mujeres</th> 
    </tr>\n""".format(len(cabecera))
    
    for codigo in diccDatosComunidades:
        if codigo in diccNombresComunidades:
            nombre = diccNombresComunidades[codigo];
        else:
            nombre = ""        
        
        columnaTabla = "\t<tr>\n\t\t <th>{} {}</th>".format(codigo,nombre)
        hombres = diccDatosComunidades[codigo].get("Hombres")
        mujeres = diccDatosComunidades[codigo].get("Mujeres")
        valores = np.concatenate((hombres,mujeres)) 
        
        for i in valores:
            columnaTabla += "<td>{}</td>".format(puntosDecimalesInt(i))
        
        columnaTabla += "\n\t</tr>\n" 
        
        cuerpoTabla += columnaTabla

    pagina += cuerpoTabla
    pagina += """</table>\n<img src="{}">\n""".format(nombreImagen)
    pagina += "</body>\n</html>"
    
    
    
    f.write(pagina)
    f.close

def obtenerDiccMediaComunidades(diccDatosComunidades,opcion):
    diccMediaComunidades = {}
    for codComunidad in diccDatosComunidades:
        media = np.mean(diccDatosComunidades[codComunidad].get(opcion))
        diccMediaComunidades.update({codComunidad: media})
    
    return diccMediaComunidades

def crearGraficoR3(diccDatosComunidades,diccNombres,mejores,año,nombreGrafico):
    
    xCod,y = zip(* mejores)
    x = []
    yHombres = []
    yMujeres = []
    posValor = añoInicio - año
    for i in range(len(xCod)):
        codComunidad = xCod[i]
        x.append(diccNombres[codComunidad])
        yHombres.append(diccDatosComunidades[codComunidad].get("Hombres")[posValor])
        yMujeres.append(diccDatosComunidades[codComunidad].get("Mujeres")[posValor])
        
    X = np.arange(len(yHombres))
    
    plt.figure("barras"+nombreGrafico, figsize=(8, 6))
    plt.title("Población de las 10 comunidades con más población media")
    plt.barh(X + 0.4, yMujeres, color = "g", height = 0.4, label = "Mujeres")
    plt.barh(X + 0.00, yHombres, color = "b", height = 0.4, label = "Hombres")
    #plt.bar(X + 0.50, datos[2], color = "r", width = 0.25)
    plt.yticks(X, x)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.xlabel("Millones de Habitantes")
    plt.ylabel("Códicgo de Comunidad Autónoma")
    plt.legend(loc='upper right')
    
    plt.savefig(carpetaDatos + nombreGrafico, bbox_inches='tight')  
    plt.show ()


def R2R3(diccNombresComunidades,diccDatosComunidades,mejores,año,nombreWeb,nombreGrafico):
    
    crearGraficoR3(diccDatosComunidades,diccNombresComunidades,mejores,año,nombreGrafico)
    generarWebComunidades(diccNombresComunidades,diccDatosComunidades,nombreWeb,nombreGrafico)
    
    #diccProvinciasComunidades = diccProvinciasComunidadesHtml(diccNombresComunidades)

def crearGraficoR5(diccDatosComunidades,diccNombres,mejores,nombreGrafico,añoElegido):
    xCod,y = zip(* mejores)
    x = []

    
    plt.figure("lineas"+nombreGrafico,figsize=(7, 6))
    años = [añoElegido]
    añoActual = añoElegido + 1
    while añoActual <= añoInicio:
        años.append(añoActual)
        añoActual += 1
    for i in range(len(xCod)):
        codComunidad = xCod[i]
        valores = diccDatosComunidades[codComunidad].get("Totales")
        valores = np.flip(valores)
        valores = valores[añoElegido - añoFinal:]
        nombre = """{} {}""".format(codComunidad, diccNombres[codComunidad])
        x.append(nombre)     
        plt.plot(años,valores[:],label = nombre)
    
    plt.title("Total de las 10 comunidades con mas media")
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.xlabel("Años")
    plt.ylabel("Millones de habitantes")
    plt.legend(loc='upper right', bbox_to_anchor=(1.52,1))
    
    plt.savefig(carpetaDatos + nombreGrafico, bbox_inches='tight') 
    plt.show ()
    
def R4R5(diccDatos,diccNombres,mejores,añoElegido,nombrePagina,nombreGrafico):
    titulo = "Apartado 4 y 5"
    tipos = ["Hombres","Mujeres"]
    
    crearGraficoR5(diccDatos,diccNombres,mejores,nombreGrafico,añoElegido)
    generarWebAbsolutaRelativa(diccDatos,diccNombres,tipos,titulo,nombrePagina,nombreGrafico)
    
    
def R6(diccDatos):
    ficheroR6 = "comunidadesAutonomasBis.htm"
    nombreWeb = "poblacionComAutonomasBis.html"
    nombreGrafico = "graficoPoblacionMediaBis.jpg";
    diccNombresComunidades, diccProvinciasComunidad, = diccComunidadesProvinciasHtml(ficheroR6)
    diccDatosComunidades = generarDiccComunidades(diccDatos,diccProvinciasComunidad)
    
    diccMediaComunidad = obtenerDiccMediaComunidades(diccDatosComunidades,"Totales") 
    mejores = Counter(diccMediaComunidad).most_common(10)
    
    
    
    R2R3(diccNombresComunidades,diccDatosComunidades,mejores,2017,nombreWeb, nombreGrafico)
    
    nombrePagina = "variacionComAutonomasBis.html"
    nombreGrafico = "graficoEvolucionPoblacionBis.jpg"
    
    R4R5(diccDatosComunidades,diccNombresComunidades,mejores,2011,nombrePagina,nombreGrafico);
    
    comproR6()

def obtenerDatosHtml(pagina,tipo):
    pagina = open(pagina, 'r', encoding=tipo)
    
    paginaString = pagina.read()
    
    
    soup = BeautifulSoup(paginaString, 'html.parser')
    celdas = soup.find_all('td')
    lista = []
    
    for celda in celdas:
        lista.append(celda.get_text())
    return lista

def comproR6():
    datosPaginaProfesor = obtenerDatosHtml("variacionProvincias2011-17.htm","ISO-8859-1")
    datosPaginaCreada = obtenerDatosHtml(carpetaDatos+"/variacionProvincias.html","utf8")
    #datosPaginaCreada[5] = 000
    if datosPaginaProfesor == datosPaginaCreada: 
        print("Los datos de las variaciones en el ejercicio 6 son igualaes") 
    else : 
        print("Los datos de las variaciones en el ejercicio 6 no igualaes")
        
        
def main():
    
    #Se crea la carpeta donde almacenaremos los datos si esta no existe.
    if not os.path.exists(carpetaDatos):
        os.mkdir(carpetaDatos)
        
    #Cargamos desde el csv los datos del csv a los diccionarios
    diccDatos, diccNombres = cargarDiccionarioCsv()

    R1(diccDatos, diccNombres)
    
    ficheroComunidades = "comunidadesAutonomas.htm"
    diccNombresComunidades, diccProvinciasComunidad, = diccComunidadesProvinciasHtml(ficheroComunidades)
    diccDatosComunidades = generarDiccComunidades(diccDatos,diccProvinciasComunidad)
    
    diccMediaComunidad = obtenerDiccMediaComunidades(diccDatosComunidades,"Totales") 
    mejores = Counter(diccMediaComunidad).most_common(10)
    
    nombreGrafico = "graficoPoblacionMedia.jpg";
    nombreWeb = "poblacionComAutonomas.html"
    print("-----------------------------------------------------------------------")
    print("Grafica del apartado 3")
    R2R3(diccNombresComunidades,diccDatosComunidades,mejores,2017,nombreWeb,nombreGrafico)
    
    nombrePagina = "variacionComAutonomas.html"
    nombreGrafico = "graficoEvolucionPoblacion.jpg"
    print("-----------------------------------------------------------------------")
    print("Grafica del apartado 4")
    R4R5(diccDatosComunidades,diccNombresComunidades,mejores,2011,nombrePagina,nombreGrafico);
    
    print("-----------------------------------------------------------------------")
    print("Graficas del apartado 6 y comprobacion de los datos de variación")
    R6(diccDatos)
    
    
if __name__== "__main__":
    main()
    