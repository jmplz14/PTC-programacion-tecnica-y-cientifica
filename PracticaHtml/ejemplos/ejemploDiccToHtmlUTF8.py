# -*- coding: utf-8 -*-
"""


@author: Eugenio

Ejemplo de tabla en HTML con CSS y pasar de diccionario a tabla en HTML

Aviso: puede haber problemas con la codificación según usemos windows o linux
por tanto en este ejemplo, optamos por usar siempre utf8 como codificación de
los ficheros.

Para tablas más complejas ver: https://www.tablesgenerator.com/html_tables
"""

fileTable=open("ejemploTabla1.html","w", encoding="utf8")

tabla1="""<!DOCTYPE html><html><head><title>Ejemplo tabla</title>
<link rel="stylesheet" href="estilo.css"> <meta charset="utf8"></head>
<body>
 <table>
  <tr>
    <th>Nombre</th>
    <th>Apellidos</th>
    <th>Edad</th>
  </tr>
  <tr>
    <td>Pepe</td>
    <td>López</td>
    <td>30</td>
  </tr>
  <tr>
    <td>Antonio</td>
    <td>García</td>
    <td>20</td>
  </tr>
</table> 
</body>
</html>"""

fileTable.write(tabla1)
fileTable.close()
print("Generada tabla html ejemploTabla1.html")


fileEstilo=open("estilo.css","w", encoding="utf8")

estilo="""  table, th, td {
                border-collapse: collapse;    
                border:1px solid black;
                font-family: Arial, Helvetica, sans-serif;
                padding: 8px;
                
            }  """

fileEstilo.write(estilo)
fileEstilo.close()






f = open('poblacionComunidades.html','w', encoding="utf8" )


paginaPob = """<!DOCTYPE html><html>
<head><title>Población</title>
<link rel="stylesheet" href="estilo.css">
<meta charset="utf8"></head>
<body><h1>Ejemplo de página de población</h1>"""

cabecera=["Comunidad", "2011", "2012", "2013"]

poblacion={"Andalucía": [6700000, 6900000, 7000000], 
           "Castilla León" : [2300000, 2350000, 2400000],
           "Aragón" : [1100000, 1200000, 1300000]}

paginaPob+= """<p><table>
<tr>"""

for nomColumna in cabecera:
    paginaPob+="<th>%s</th>" % (nomColumna)

paginaPob+="</tr>"


for comunidad, habitantes in sorted(poblacion.items()):
    paginaPob+="<tr><td>%s</td>" % (comunidad)
    for habitantesAnio in habitantes:
        paginaPob+="<td>%d</td>" % (habitantesAnio)
    paginaPob+="</tr>"

        

paginaPob+="</p></body></html>"

f.write(paginaPob)
f.close()
print("Generada tabla html poblacionComunidades.html")

''' La sustitución con % se suele usar con %s string %d entero %f float '''

# Formateo con str.format()
# -------------------------

# El formato con str.format() permite fijar la longitud de
# una cadena, aplicar formatos numéricos, establecer la 
# alineación, tabular datos y rellenar espacios con un 
# determinado caracter:

# Aplica formatos numéricos ajustando la precisión:

valor1 = 867.56767  # asigna flotante
valor2 = 989.45548  # asigna flotante
print('El primer valor es {0:10.5}, el segundo es {1:10.5}'.format(valor1, valor2))  # 8.57 9.455
 
