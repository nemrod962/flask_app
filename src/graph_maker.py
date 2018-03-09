# -*- coding: UTF-8 -*-
from flask import Flask
#graficas
import pygal
from pygal.style import DarkSolarizedStyle
#numeros aleatorios
import random
#nombre de la base de datos utilizada
import web_functions
#formato y conversion fechas
import date_handler
 
app = Flask(__name__)

"""
Clase encargada de dibujar grafos con los 
datos contenidos en las bases de datos sobre
los numeros aleatorios.

Recibiremos las listas con los valores de los numeros 
y sus fechas de obtencion. A partir de ellas generaremos
las graficas.

"""
class GraphMaker:
    
    #Crea un grafo de lineas con las listas 
    #de numeros y fechas proporcionadas.
    #Las listas las obtenemos de DBHandler,
    #que sera una instancia de SQLHandler
    #o de BeeHandler. Ambas clases contienen
    #las listas listaGlobalNumero y
    #listaGlobalFecha.
    #Accesibles mediante DBHandler.listaGlobal...
    def crearGrafo(self, DBHandler, tipo=None):

        #Parametros de la grafica
        anchura = 900
        altura = 900
        tam_explicito = True
        
        #Obtengo las listas de los numeros y su tiempo de obtencion
        #Aqui no obtengo una copia, si no que referencio a las mismas listas.
        #listaNumeros = DBHandler.listaGlobalNumero
        #listaFechas = DBHandler.listaGlobalFecha
        #De esta forma obtengo una copia de las listas.
        #Así puedo operar con ellas y transformarlas de forma
        #que no afecten a otras partes del programa.
        listaNumeros = list(DBHandler.listaGlobalNumero)
        listaFechas = list(DBHandler.listaGlobalFecha)
        
        #Obtengo que DB estoy empleando
        dbname = web_functions.getDBSimpleName(DBHandler)

        #Si la base de datos empleada es Beebotte, en las listas de
        #numeros y fechas estan los mas recientes en las primeras posiciones.
        #Para hacer bien la grafica, tendremos que invertir ambas listas
        if dbname == "beebotte":
            #dar vuelta
            listaNumeros.reverse()
            listaFechas.reverse()

        #Cambio el formato de las fechas, de ms a formato fecha
        for indice in xrange(len(listaFechas)):
            listaFechas[indice] = date_handler.msToDatetime(listaFechas[indice])

        #graph = pygal.Line(\
        #width = anchura,\
        #height=altura,\
        #explicit_size=tam_explicito)

        #SELECCIONO TIPO DE GRAFO

        if str(tipo).lower() == "bar":
            #print "TIPO: BARRAS"
            graph = pygal.Bar()
        #Si la string recibida definiendo el tipo no es 'bar',
        #supongo que el tipo deseado es 'line'. Si recibimos una
        #cadena diferente a cualquiera de las opciones, utilizaremos
        #el grafo de líneas por defecto.
        else:
            #print "TIPO: LINEAS"
            graph = pygal.Line()

        graph.title = 'Grafo ' + dbname
        graph.x_labels = listaFechas
        graph.add('Numeros Aleatorios', listaNumeros)
        #Es necesario poner is_unicode=True para que la aplicacion
        #pueda insertar adecuadamente el grafo en el html template.
        graph_data = graph.render(is_unicode=True) 

        #print graph_data

        return graph_data


