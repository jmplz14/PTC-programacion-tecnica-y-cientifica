#!/usr/bin/env python3.7
# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 15:56:53 2019

@author: jose
"""

import numpy as np
import locale
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


""" Crea dos diccionarios. Uno contendran el codigo con el nombre y otro el codigo con los datos
    Parameters:
    Returns:
        -diccionarioDatos: Diccionario con la estructura {Codigo:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -diccionarioNombres: Diccionario con la estructura {Codigo:Nombre}
        
"""
def cargarDiccionarioCsv():
    
    #abrmios el cs, carmagos en un string los datos y lo cerramos.
    ficheroInicial=open("poblacionProvinciasHM2010-17.csv","r", encoding="ISO-8859-1")
    cadenaPob=ficheroInicial.read()    
    ficheroInicial.close()
    
    #limpiamos la cabecera y la parte final que no nos haran falta.
    primero=cadenaPob.find("Total Nacional;")
    ultimo=cadenaPob.find("Notas")    
    cadenaFinal=cadenaPob[primero:ultimo-1]
    
    #hacermos un explit por lineas para recorrer linea a line el string ya limpiado
    i = 0  
    for line in cadenaFinal.splitlines():
        #creamos una lista con los datos separados por ;
        arrayDatos = line[:-1].split(";")
        
        #Si i es igual a 0 será la primera pasada y seran los datos del total nacional.
        if i == 0:
            diccionarioDatos = {arrayDatos[0]: {"Totales": arrayDatos[1:9], "Hombres": arrayDatos[9:17], "Mujeres": arrayDatos[17:]}}
            #Sumamos 1 a i para saaber que ya tenemos guardados el total nacional
            i += 1
        #En el else ya trabajamos los datos por provincia
        else:
            
            #Separamos el código del nombre de la provincia diferenciando uno del otro por el primer espacio
            codigoNombre = arrayDatos[0].split(" ",1)
            
            #Si i es igual a 1 sera la primera provincia y crearemos el diccionarioNombres
            if i == 1:
                diccionarioNombres = {codigoNombre[0]: codigoNombre[1]}
                i += 1
            #en else ya tendremos el diccionario de nombres creado y solo tendremos que ir añadiendo.
            else:
                diccionarioNombres.update({codigoNombre[0]: codigoNombre[1]})
            
            #Añadimos los valores de cada provincia al diccionario segun su codigo.
            diccionarioDatos.update({codigoNombre[0]: {"Totales": arrayDatos[1:9], "Hombres": arrayDatos[9:17], "Mujeres": arrayDatos[17:]}})
               
    return diccionarioDatos,diccionarioNombres


""" Crea una pagina web con los datos dados por dos diccionarios
    Parameters:
        -diccDatos: Diccionario con la estructura {Codigo:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -diccNombres: Diccionario con la estructura {Codigo:Nombre}
        -tipos: Lista con los tipos que vamos a mostrar en la tabla. Puede contener Totales, Hombres o Mujeres o
        varios de ellos
        -titulo: El titulo que tendra la pagina web.
        -fichero: Fichero en el que se guardara la pagina.
        -imagen: imagen que añadiremos a la web.
    Returns:
"""
def generarWebAbsolutaRelativa(diccDatos,diccNombres,tipos,titulo,fichero,imagen = None):
    
    #Obtenemos el numero de tipos que añadiremos
    numTipos = len(tipos)
    
    #obtenemos los datos con las variacciones absolutas y relativas
    diccVarRelativa, diccVarAbsoluta = obtenerDiccVariacion(diccDatos,tipos)
    
    #abrimos el fichero de la web
    f = open(carpetaDatos + fichero,'w', encoding="utf8" )
    
    #creamos el head y inicamos el cuerpo y la tabla
    pagina = """<!DOCTYPE html><html>
    <head><title>{}</title>
    <link rel="stylesheet" href="../estilo.css">
    <meta charset="utf8"></head>
    <body>
    <table>""".format(titulo)
    
    #años que se usaran como cabecera de tabla
    cabecera = ["2017","2016","2015","2014","2013","2012","2011"]
    
    #iniciamos la cabecera de la tabla con los años
    cabeceraHtml = """\n\t<tr>\n\t\t<th> </th>"""
    #por cada  tipo que realicemos las variaciones necesitaremos mostrar dos veces los años, 
    #una para relativa y otra para absoluta.
    for i in range(numTipos * 2):
        for i in cabecera:
            cabeceraHtml += """\t<th>{}</th>""".format(i)
    #terminamos la cabecera de los años par ala tabla
    cabeceraHtml += "\n\t</tr>\n"

    #La añadimos al string donde alamcenamos la pagina
    pagina += cabeceraHtml

    #numero de años que tendremos
    numAños = len(cabecera)
    
    #Si hay mas de un tipo los añadiremos debajo de laos años con 
    if numTipos > 1:
        #inicamos la cabecera de tipos y añadimos cada uno de los tipos.
        cabeceraTipos = """\n\t<tr>\n\t\t<th> </th>"""
        for tipo in tipos:
            cabeceraTipos += """\t<th colspan="{}" >{}</th>""".format(numAños * 2,tipo)
            
        cabeceraTipos += "\n\t</tr>\n"
        
        #La añadimos al string donde alamcenamos la pagina
        pagina += cabeceraTipos
    
    
    cuerpoTabla = """<tr>
    <th> </th> """ 
    
    #añadimos otra conlumna que nos indique si la parte de la relativa o de la absoluta
    #se añde tantas veces como tipos tengamos
    for i in range(numTipos):
        cuerpoTabla +="""<th colspan="{0}" >Absoluta</th> <th colspan="{0}">Relativa</th>""".format(numAños)
        
    cuerpoTabla += "\n</tr>\n"
    
    
    #recoremos el diccionario diccDatos para ir cargando los datos de cada provincia a la tabla.
    for codigo in diccDatos:
        #si el codigo esta en el diccionario de nombres el guardaremos el nombre, sino sera vacio
        #por ejemplo el total nacional no tendria un nombre y entraria en el else. En cambio
        #cada codigo de provincia si tendria un nombre de provincia y este se guardaria.
        if codigo in diccNombres:
            nombre = diccNombres[codigo];
        else:
            nombre = ""
        
        #añadimos a la tabla el nombre este dato del diccionario.
        columnaTabla = "\t<tr>\n\t\t <th>{} {}</th>".format(codigo,nombre)
        
        #Nos quedamos con sus valores para absoluta y relativa
        absoluta = diccVarAbsoluta[codigo]
        relativa = diccVarRelativa[codigo]
        
        #si tenemos varios tipos recorremermos varias veces
        for posTipo in range(numTipos):
            
            #añadimos cada dato de la absoluta para este tipo
            for i in range(numAños):
                pos = posTipo * numAños + i
                #print(pos)
                columnaTabla += "<td>{}</td>".format(puntosDecimalesInt(absoluta[pos]))
                
            #añadimos cada dato de la relativa para este tipo
            for i in range(numAños):
                pos = posTipo * numAños + i
                columnaTabla += "<td>{}</td>".format(puntosDecimalesFloat(relativa[pos]))
                
        #terminaos esta columna      
        columnaTabla += "\n\t</tr>\n" 
        cuerpoTabla += columnaTabla
    #añadimo todas las columnas a la pagina y cerramos la tabla
    pagina += cuerpoTabla + "</table>\n"
    
    #Si pasamos imagen la añadimos  despues de la tabla
    if imagen != None:
        pagina += """<img src="{}">\n""".format(imagen)

    #cerramos el body y el html para terminar la pagina  
    pagina += "</body>\n</html>"
    
    #Escribimos y cerramos el fichero
    f.write(pagina)
    f.close
    
    
""" Realiza el apartado 1 de la practica.
    Parameters:
        -diccionarioDatos: Diccionario con la estructura {Codigo:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -diccionarioNombres: Diccionario con la estructura {Codigo:Nombre}
    Returns:
"""    
def R1(diccDatos, diccNombres):
    
    #Inicaimos los valores para el titulo la pagina que leeremos.
    titulo = "Apartado 1"
    pagina = "variacionProvincias.htm"
    
    #añadicmos los tipos que queremos mostrar.
    tipos = ["Totales"]
    generarWebAbsolutaRelativa(diccDatos,diccNombres,tipos,titulo,pagina)


""" Obtiene los diccionarios con los valores de las variaciones y los devuelve.
    Parameters:
        -diccDatos: Diccionario con la estructura {Codigo:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -tipos: Lista con los tipos que vamos a mostrar en la tabla. Puede contener Totales, Hombres o Mujeres o
        varios de ellos
    Returns:
        -diccDatosVarRelativa: Diccionario con la estructra {codigoProvincia: []} el array almacena varianza relativa
        -diccDatosVarAbsoluta: Diccionario con la estructra {codigoProvincia: []} el array almacena varianza absoluta
"""     
def obtenerDiccVariacion(diccDatos,tipos):
    
    #iniciamos los dos diccionarios vacios
    diccDatosVarAbsoluta = {}
    diccDatosVarRelativa = {}
    
    #Recorremos la lista de tipos
    for tipo in tipos:
        #recorremos los codigos del diccionario de datos
        for codProvincia in diccDatos:
            #Nos queamos el array con los datos dle tipo correspondiente
            datosActuales = diccDatos[codProvincia].get(tipo);    
            
            #Guardamos el número de elementos -1 que para la variaciones tendremos un valor menos
            numElementos = len(datosActuales) - 1
            
            #Creamos dos arrays para alamacenar ambas variaciones.
            datosVarAbsoluta = np.empty(numElementos)
            datosVarRelativa = np.empty(numElementos)
            
            #Realizamos las operaciones para obtener las variaciones
            for i in range(numElementos):
                #obtenemos las variaciones con los datos de la posición i y i-1
                valorAbsoluta = int(float(datosActuales[i]) - float(datosActuales[i+1]))
                valorRelativa = (valorAbsoluta / float(datosActuales[i+1])) * 100
                
                #guardamos los datos de las variaciones
                datosVarAbsoluta[i] = valorAbsoluta
                datosVarRelativa[i] = valorRelativa
            
            #Si ya tenemos tenemos este codigo de pronvincia es que ya se añadio datos de otro tipo
            if codProvincia in diccDatosVarAbsoluta.keys():
                #copiamos los datos de la absoluta y añadimos los nuevos datos
                valores = np.concatenate((diccDatosVarAbsoluta[codProvincia] ,datosVarAbsoluta))
                diccDatosVarAbsoluta.update({codProvincia: valores})
                
                #copiamos los datos de la relativa y añadimos los nuevos datos
                valores = np.concatenate((diccDatosVarRelativa[codProvincia] ,datosVarRelativa))                
                diccDatosVarRelativa.update({codProvincia: valores})
            #Si no existe el codigo de provincia es que aun no introducimos datos
            else:
                #Introducimos los datos nuevos
                diccDatosVarAbsoluta.update({codProvincia: datosVarAbsoluta})
                diccDatosVarRelativa.update({codProvincia: datosVarRelativa}) 
                
                
    return diccDatosVarRelativa, diccDatosVarAbsoluta
        
        
""" Obtenemos las comunidad y las provincias que pertenece de cada diccionario
    Parameters:
        -fichero: fichero del que cogeremos los datos
    Returns:
        -diccNombresComunidad: Diccionario con la estructra {codigoComAutonomica: NombreComAutonomica} 
        -diccProvinciasComunidad:  Diccionario con la estructra {codigoComAutonomica: []} el array contiene
        diccionarios con la estructura {codProvincia: nombreProvincia}.
"""
def diccComunidadesProvinciasHtml(ficheroComunidades):
    
    numColumnas = 4
    
    #Cargamos los ficheros necesarios y los guardamos en un string
    comunidadesFich = open(ficheroComunidades, 'r', encoding="ISO-8859-1")
    provinciasFich = open('comunidadAutonoma-Provincia.htm', 'r', encoding="ISO-8859-1") 
    comString = comunidadesFich.read()
    provString = provinciasFich.read()
    
    #recogemos todos los td de la tabla de comunidades
    soup = BeautifulSoup(comString, 'html.parser')
    valores = soup.find_all('td')
    
    #inicializamos los diccionarios a devolver
    diccNombresComunidad = {}
    diccProvinciasComunidad = {}
    
    #recorremos los ted de comunidades cogiendo datos de dos en dos
    for i in range(0,len(valores)//2):
        pos = i * 2
        
        #cogemos el codigo y el nombre de cada td
        codigo = valores[pos].get_text()
        codigo = codigo[:-1]
        nombre = valores[pos+1].get_text()
        
        #añadimos la comunidad autonoma al diccionario que las almacen con el nombre
        diccNombresComunidad.update({codigo: nombre})
        
        #vamos inicializando a vacio el diccionario que contendra el codigo de comunidad autonoma
        #y las lista de provincias de cada comunidad autonoma 
        diccProvinciasComunidad.update({codigo: {}})
    
    #Cogemos los td de la tabla de provincias y comunidades autonomas
    soup = BeautifulSoup(provString, 'html.parser')
    valores = soup.find_all('td')
    
    #limpio para limpar una fila que no es valida
    for i in range(3):
        valores.pop(50 * numColumnas)
    
    #recorremos los td de 4 en cuatro
    for i in range(len(valores)//numColumnas):
        pos = i * 4
        
        #nos quedamos con los valores para la comunidad y provincia
        codigoComunidad = valores[pos].get_text()
        codigoComunidad = codigoComunidad.replace(" ","")
        codigoProvincia = valores[pos+2].get_text()
        codigoProvincia = codigoProvincia.replace(" ","")
        nombreProvincia = valores[pos+3].get_text()
        #print(i)
        
        #si el ccodigo de Comunidad fue de los que introducimos en nuestro diccionario al recorrelos seran añadidos
        if codigoComunidad in diccProvinciasComunidad.keys():
            
            #obtengo el diccionario con los codigo de provincias y nombres que corresponde a esa comunidad
            valoresComunidad = diccProvinciasComunidad[codigoComunidad]
            
            #añadimos a estos la nueva provincia y los actualizamos en el diccionario de provincias
            valoresComunidad.update({codigoProvincia:nombreProvincia})           
            diccProvinciasComunidad.update({codigoComunidad: valoresComunidad})
        
  
    return diccNombresComunidad, diccProvinciasComunidad

""" Sumamos una lista de numeros alamacenados como string y un array de numpy
    Parameters:
        -strings: Lista de numeros alamacenados como string
        -numeros: array numpy 
    Returns:
        -Array numpy con la suma de numeros + strings
       
"""   
def sumarArrayStringYNumpi(strings,numeros):
    #convertimos strings en un vector de numpy con float
    stringNumerico = np.array(strings)
    stringNumerico = stringNumerico.astype(np.float)
    
    #devolvemos la suma de los dos arrays
    return numeros + stringNumerico


""" Obtenemos los datos de poblacion para las comunidades autóomas
    Parameters:
        -diccDatos: Diccionario con la estructura {Codigo:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -diccProvinciasComunidad:  Diccionario con la estructra {codigoComAutonomica: []} el array contiene
        diccionarios con la estructrua {codProvincia: nombreProvincia}.
    Returns:
        -diccDatosComunidades: : Diccionario con la estructura {codigoComAutonoma:{"Totales":[], "Hombres":[] "Mujeres":[]}}
       
"""       
def generarDiccComunidades(diccDatos,diccProvinciasComunidad):
    #inicamos el diccionario vacio
    diccDatosComunidades = {}
    
    #recorremos el diccionario con las provincias de cada comunidad autónoma
    for codComunidad in diccProvinciasComunidad:
        #inicamos el vector en el que almacenaremos los valores totales de poblacion
        datosTotales = {"Totales":np.zeros(8),"Hombres":np.zeros(8),"Mujeres":np.zeros(8),}
        
        #recorremos la lista de provincias que tiene cada comunidad autonoma
        for codProvincia in diccProvinciasComunidad[codComunidad]:
            #obtenemos los datos de poblacion de la provincia
            datosProvincia = diccDatos[codProvincia]
            
            #sumamos los datos de cada provincia a los totales de la comunidad para los tres tipos
            suma = sumarArrayStringYNumpi(datosProvincia["Totales"],datosTotales["Totales"])
            datosTotales["Totales"] = suma           
            suma = sumarArrayStringYNumpi(datosProvincia["Hombres"],datosTotales["Hombres"])
            datosTotales["Hombres"] = suma         
            suma = sumarArrayStringYNumpi(datosProvincia["Mujeres"],datosTotales["Mujeres"])
            datosTotales["Mujeres"] = suma
            
        #añadimos los totales al diccionara con los datos de cada comunidad
        diccDatosComunidades.update({codComunidad: datosTotales})
        
    return diccDatosComunidades
            
            
            
            
def obtenerStringCsvNumpy(valores):
    stringCsv = ""
    for valor in valores:
        stringCsv += "{};".format(str(valor))
    return stringCsv

""" Crea la web para el apartado 2 con los totales por comunidad
    Parameters:
        -diccNombresComunidades: Diccionario con la estructura {codigoComAutonoma:Nombre}
        -diccDatosComunidades: Diccionario con la estructura {codigoComAutonoma:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -nombreWeb: Fichero en el que se guardara la pagina.
        -imagen: imagen que añadiremos a la web.
        -nombreImagen: nombre del grafico a insertar
    Returns:
"""            
def generarWebComunidades(diccNombresComunidades,diccDatosComunidades,nombreWeb,nombreImagen):
    #abrimos el fichero en el que se alamacnara el html
    f = open(carpetaDatos + nombreWeb,'w', encoding="utf8" )
    
    #iniciamos el html, head, boyd y table de la web
    pagina = """<!DOCTYPE html><html>
    <head><title>Apartado 2 y 3</title>
    <link rel="stylesheet" href="../estilo.css">
    <meta charset="utf8"></head>
    <body>
    <table>"""
    
    
    cabecera = ["2017","2016","2015","2014","2013","2012","2011","2010"]
    
    #creamos la fila con los años para la tabla, necesitaremos repetirla dos veces una para hombres y otra para mujeres
    cabeceraHtml = """\n\t<tr>\n\t\t<th> </th>"""
    for i in range(2):
        for i in cabecera:
            cabeceraHtml += """\t<th>{}</th>""".format(i)
    
    cabeceraHtml += "\n\t</tr>\n"
    
    #añadimos los años al html
    pagina += cabeceraHtml

    #creamos la fila que nos marcara el apartado de datos de hombres y mujeres
    cuerpoTabla = """<tr>
    <th> </th> <th colspan="{0}" >Hombres</th> <th colspan="{0}">Mujeres</th> 
    </tr>\n""".format(len(cabecera))
    
    #empezamos a crear los datos par ala tabla
    for codigo in diccDatosComunidades:
        
        #obtenemos el nombre de la comunidad y lo añadimos a la fila
        nombre = diccNombresComunidades[codigo];
        filaTabla = "\t<tr>\n\t\t <th>{} {}</th>".format(codigo,nombre)
        
        #obtenemos los datos de los hombres y mujeres para esa comunidad y los concatenamos en un array
        hombres = diccDatosComunidades[codigo].get("Hombres")
        mujeres = diccDatosComunidades[codigo].get("Mujeres")
        valores = np.concatenate((hombres,mujeres)) 
        
        #recorremos los valores y los vamos añadiendo a la fila
        for i in valores:
            filaTabla += "<td>{}</td>".format(puntosDecimalesInt(i))
        
        #ceramos la fila y la añadimos a la tabla
        filaTabla += "\n\t</tr>\n" 
        cuerpoTabla += filaTabla
    
    #añadimos la tabla al html y añadimos la imagen de la grafica
    pagina += cuerpoTabla
    pagina += """</table>\n<img src="{}">\n""".format(nombreImagen)
    pagina += "</body>\n</html>"
    
    
    #escribimos el html y cerramos el fichero
    f.write(pagina)
    f.close

""" Se calcula la media de cada comunidad autónoma para Totales, Hombres o Mujeres dependiendo de la opcion
    Parameters:
        -diccDatosComunidades: Diccionario con la estructura {codigoComAutonoma:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -opcion: String que nos indicara la opcion de la que queremos obtener la media.
    Returns:
        -diccMediaComunidades: diccionario con la estructura {codigoComAutonoma: media}  
"""
def obtenerDiccMediaComunidades(diccDatosComunidades,opcion):
    #inciamos el diccionario de media
    diccMediaComunidades = {}
    
    #Recorremos todas las comunidades
    for codComunidad in diccDatosComunidades:
        #calculamos la media y la añadimos al diccionario de medias
        media = np.mean(diccDatosComunidades[codComunidad].get(opcion))
        diccMediaComunidades.update({codComunidad: media})
    
    return diccMediaComunidades

""" Se realiza el grafico para el apartado 3
    Parameters:
        -diccDatosComunidades: Diccionario con la estructura {codigoComAutonoma:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -diccNombres: Diccionario con la estructra {codigoComAutonomica: NombreComAutonomica}
        -mejores: Lista de tuplas que contiene (codigoComAutonoma, media) 
        -año: Año para mostrar los datos de la grafica
        -nombreGrafico: nombre con el que guardaremos la grafica
    Returns:
"""
def crearGraficoR3(diccDatosComunidades,diccNombres,mejores,año,nombreGrafico):
    
    #separamos la tupa de mejores
    xCod,y = zip(* mejores)
    
    #inicalizamos los array donde almacenaremos los valores para los datos de poblacion y x que tendra los nombres
    #de las comunidades
    x = []
    yHombres = []
    yMujeres = []
    
    #calculamos la posicion en la que tendremos el año
    posValor = añoInicio - año
    
    #recorremos los codigos de las comunidades
    for i in range(len(xCod)):
        codComunidad = xCod[i]
        
        #añadimos el nombre de la comunidad a x
        x.append(diccNombres[codComunidad])
        
        #añadimos los datos de polbacion tanto para hombres como para mujeres
        yHombres.append(diccDatosComunidades[codComunidad].get("Hombres")[posValor])
        yMujeres.append(diccDatosComunidades[codComunidad].get("Mujeres")[posValor])
    
    #iniciamos la x que nos situara las barras en el grafico
    X = np.arange(len(yHombres))
    
    #generamos la grafica
    plt.figure("barras"+nombreGrafico, figsize=(8, 6))
    plt.title("Población de las 10 comunidades con más población media")
    plt.barh(X + 0.4, yMujeres, color = "g", height = 0.4, label = "Mujeres")
    plt.barh(X + 0.00, yHombres, color = "b", height = 0.4, label = "Hombres")
    plt.yticks(X, x)
    plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
    plt.xlabel("Millones de Habitantes")
    plt.ylabel("Códicgo de Comunidad Autónoma")
    plt.legend(loc='upper right')
    
    #guardamos y mostramos el grafico
    plt.savefig(carpetaDatos + nombreGrafico, bbox_inches='tight')  
    plt.show ()


""" Se realiza el grafico y la web de los apartados 2 y 3
    Parameters:
        -diccNombresComunidades: Diccionario con la estructra {codigoComAutonomica: NombreComAutonomica}
        -diccDatosComunidades: Diccionario con la estructura {codigoComAutonoma:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -mejores: Lista de tuplas que contiene (codigoComAutonoma, media) 
        -año: Año para mostrar los datos de la grafica
        -nombreWeb: nombre del fichero en el que alamacenaremos la web
        -nombreGrafico: nombre con el que guardaremos la grafica
    Returns:
"""
def R2R3(diccNombresComunidades,diccDatosComunidades,mejores,año,nombreWeb,nombreGrafico):
    
    #creamos la grafica para el apartado 3
    crearGraficoR3(diccDatosComunidades,diccNombresComunidades,mejores,año,nombreGrafico)
    #creamos la web para el apartado 2
    generarWebComunidades(diccNombresComunidades,diccDatosComunidades,nombreWeb,nombreGrafico)
    
""" Se crea el grafico del apartado 5 de la practica
    Parameters:
        -diccDatosComunidades: Diccionario con la estructura {codigoComAutonoma:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -diccNombres: Diccionario con la estructra {codigoComAutonomica: NombreComAutonomica}
        -mejores: Lista de tuplas que contiene (codigoComAutonoma, media) 
        -nombreGrafico: nombre con el que guardaremos la grafica
        -añoElegido: Año elegido para iniciar la grafica
    Returns:
""" 
def crearGraficoR5(diccDatosComunidades,diccNombres,mejores,nombreGrafico,añoElegido):
    
    #separamos la tupla quedandonos con el codigo de comunidad en xCod
    xCod,y = zip(* mejores)
    #x = []

    #inicamos la grafica
    plt.figure("lineas"+nombreGrafico,figsize=(7, 6))
    
    #creamos las etiquetas para el eje de la grafica de años inicial solo con el año elegido de inicio
    #termina en el utlimo año
    años = [añoElegido]
    añoActual = añoElegido + 1
    while añoActual <= añoInicio:
        años.append(añoActual)
        añoActual += 1
        
    #recorremos el array que tiene el codigo de las comunidades aoutonomas
    for i in range(len(xCod)):
        #guardamos el codigo de la comunidad y cogemos los totales
        codComunidad = xCod[i]
        valores = diccDatosComunidades[codComunidad].get("Totales")
        
        #los invertimos porque nos interesa mostrarlos en sentido contrario y eliminamos los años que no mostraremos
        valores = np.flip(valores)
        valores = valores[añoElegido - añoFinal:]
        
        #nos quedamos el nombre de la comunidad aoutonoma para y el codigo y lo añadimos al label
        nombre = """{} {}""".format(codComunidad, diccNombres[codComunidad])
        plt.plot(años,valores,label = nombre)
    
    #rellenamos los titulos y opiciones del grafico
    plt.title("Total de las 10 comunidades con mas media en 2017")
    plt.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
    plt.xlabel("Años")
    plt.ylabel("Millones de habitantes")
    plt.legend(loc='upper right', bbox_to_anchor=(1.52,1))
    
    #guardamos y dibujamos el grafico
    plt.savefig(carpetaDatos + nombreGrafico, bbox_inches='tight') 
    plt.show ()

""" Se realiza el grafico y la web de los apartados 4 y 5
    Parameters:
        -diccDatos: Diccionario con la estructura {codigoComAutonoma:{"Totales":[], "Hombres":[] "Mujeres":[]}}
        -diccNombres: Diccionario con la estructra {codigoComAutonomica: NombreComAutonomica}
        -mejores: Lista de tuplas que contiene (codigoComAutonoma, media) 
        -añoElegido: Año elegido para iniciar la grafica
        -nombrePagina: nombre del fichero en el que alamacenaremos la web
        -nombreGrafico: nombre con el que guardaremos la grafica
    Returns:
"""   
def R4R5(diccDatos,diccNombres,mejores,añoElegido,nombrePagina,nombreGrafico):
    #titulo de la web
    titulo = "Apartado 4 y 5"
    tipos = ["Hombres","Mujeres"]
    
    #creamos la grafica del apartado 5
    crearGraficoR5(diccDatos,diccNombres,mejores,nombreGrafico,añoElegido)
    
    #creamos la web del apartado 4
    generarWebAbsolutaRelativa(diccDatos,diccNombres,tipos,titulo,nombrePagina,nombreGrafico)
    

""" Se realiza el apartado 6
    Parameters:
        -diccDatos: Diccionario con la estructura {Codigo:{"Totales":[], "Hombres":[] "Mujeres":[]}}
    Returns:
"""   
def R6(diccDatos):
    
    ficheroR6 = "comunidadesAutonomasBis.htm"
    nombreWeb = "poblacionComAutonomasBis.htm"
    nombreGrafico = "graficoPoblacionMediaBis.jpg"
    
    #obtenemos los codigos, nombres y provincias de las comunidades autonomas
    diccNombresComunidades, diccProvinciasComunidad, = diccComunidadesProvinciasHtml(ficheroR6)
    diccDatosComunidades = generarDiccComunidades(diccDatos,diccProvinciasComunidad)
    
    #obtenemos la media de los totales de estas comunidades y nos quedamos ocn las 10 mejores
    diccMediaComunidad = obtenerDiccMediaComunidades(diccDatosComunidades,"Totales") 
    mejores = Counter(diccMediaComunidad).most_common(10)
    
    
    #llamamos a la funcion del apartado 2 y 3 para crear la web y el grafico
    R2R3(diccNombresComunidades,diccDatosComunidades,mejores,2017,nombreWeb, nombreGrafico)
    
    nombrePagina = "variacionComAutonomasBis.htm"
    nombreGrafico = "graficoEvolucionPoblacionBis.jpg"
    
    #llamamos a la funcion del apartado 4 y 5 para crear la web y el grafico
    R4R5(diccDatosComunidades,diccNombresComunidades,mejores,2011,nombrePagina,nombreGrafico);
    
    #Comprobación de los datos
    comproR6()
""" Carga los td de una tabla a una lista y devuelve esta
    Parameters:
        -pagina: nombre de la pagina que abireremos
        -tipo: Formato del fichero
    Returns:
        -lista: Lista de string con los valores que contienen los td de la tabla
"""   
def obtenerDatosHtml(pagina,tipo):
    #abrimos la pagina
    pagina = open(pagina, 'r', encoding=tipo)
    
    #la leemos y alamacenamos en un string
    paginaString = pagina.read()
    
    #obtenemos los td de la pagina
    soup = BeautifulSoup(paginaString, 'html.parser')
    celdas = soup.find_all('td')
    
    #recorremos todos los td obtenidos y vamos guardando el testo de estos en un td
    lista = []
    for celda in celdas:
        lista.append(celda.get_text())
        
    pagina.close()
    return lista

""" Se realiza la comprobación de que las varianzas calculadas en el apartado 1 correspondan
    con las dadas por el profesor
    Parameters:
    Returns:
"""   
def comproR6():
    
    #obtenemos los datos de las dos paginas web
    datosPaginaProfesor = obtenerDatosHtml("variacionProvincias2011-17.htm","ISO-8859-1")
    datosPaginaCreada = obtenerDatosHtml(carpetaDatos+"variacionProvincias.htm","utf8")
    
    #comparamos las dos listas con los datos
    if datosPaginaProfesor == datosPaginaCreada: 
        print("Los datos de las variaciones de la pagina dada como ejemplo y la generada son iguales") 
    else : 
        print("Los datos de las variaciones de la pagina dada como ejemplo y la generada no son iguales") 
        
        
def main():
    
    #Se crea la carpeta donde almacenaremos los datos si esta no existe.
    if not os.path.exists(carpetaDatos):
        os.mkdir(carpetaDatos)
        
    #Cargamos desde el csv los datos del csv a los diccionarios
    diccDatos, diccNombres = cargarDiccionarioCsv()

   #Realizamos el primer apartado
    R1(diccDatos, diccNombres)
    
    ficheroComunidades = "comunidadesAutonomas.htm"
    
    #cargamos los nombres de las comunidades y sus codigos y las provincias que pertenece a cada comunidad 
    diccNombresComunidades, diccProvinciasComunidad, = diccComunidadesProvinciasHtml(ficheroComunidades)
    #obtenemos los datos de cada comunidad autonoma(Totales, Hombres y MUjeres)
    diccDatosComunidades = generarDiccComunidades(diccDatos,diccProvinciasComunidad)
    
    #obtenemos la media de la poblacion para todas las comunidades
    diccMediaComunidad = obtenerDiccMediaComunidades(diccDatosComunidades,"Totales") 

    #obtenemos las 10 comunidades con mas poblacion media
    mejores = Counter(diccMediaComunidad).most_common(10)
    
    nombreGrafico = "graficoPoblacionMedia.jpg";
    nombreWeb = "poblacionComAutonomas.htm"
    
    print("-----------------------------------------------------------------------")
    print("Grafica del apartado 3")

    #realizamos lo propuesto en el apartado dos y tres.
    R2R3(diccNombresComunidades,diccDatosComunidades,mejores,2017,nombreWeb,nombreGrafico)
    
    
    nombrePagina = "variacionComAutonomas.htm"
    nombreGrafico = "graficoEvolucionPoblacion.jpg"
    print("-----------------------------------------------------------------------")
    print("Grafica del apartado 4")
    R4R5(diccDatosComunidades,diccNombresComunidades,mejores,2011,nombrePagina,nombreGrafico);

    print("-----------------------------------------------------------------------")
    print("Graficas del apartado 6 y comprobacion de los datos de variación")
    R6(diccDatos)
    
    
if __name__== "__main__":
    main()
    