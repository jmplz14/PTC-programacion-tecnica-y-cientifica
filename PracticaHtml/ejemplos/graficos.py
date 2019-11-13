# -*- coding: utf-8 -*-
"""
Created on Wed Nov  7 18:47:40 2018

@author: Eugenio
"""

import numpy as np
import matplotlib.pyplot as plt

lista1 = [11,2,3,15,8,13,21,34] # Declara lista1 con 8 valores

plt.figure("lineal")
plt.plot(lista1)   # Dibuja el gráfico
plt.title("Título")   # Establece el título del gráfico
plt.xlabel("abscisa")   # Establece el título del eje x
plt.ylabel("ordenada")   # Establece el título del eje y

plt.savefig("Grafico1.jpg")

datos = [[1, 2, 3, 4], [3, 5, 3, 5], [8, 6, 4, 2]]
X = np.arange(4)

plt.figure("barras")
plt.barh( X + 0.00,datos[0], color = "b", height= 0.25)
plt.barh( X + 0.25,datos[0], color = "g", height= 0.25)
plt.barh( X + 0.50,datos[0], color = "r", height= 0.25)
plt.yticks(X+0.38, ["A","B","C","D"])

plt.savefig("Grafico2.jpg")

plt.figure("circular")
impr = ["b/n", "color", "dúplex", "A3"]
vol = [25, 31, 46, 10]
expl =(0, 0.05, 0, 0)
plt.pie(vol, explode=expl, labels=impr, autopct='%1.1f%%', shadow=True)
plt.title("Impresión", bbox={"facecolor":"0.8", "pad":5})
plt.legend()

plt.savefig("Grafico3.jpg")








# Más información en
#https://programacion.net/articulo/introduccion_a_la_libreria_matplotlib_de_python_1599
#https://python-para-impacientes.blogspot.com/2014/08/graficos-en-ipython.html
