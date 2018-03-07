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
    def crearGrafo(self, DBHandler):
        
        #Obtengo las listas de los numeros y su tiempo de obtencion
        listaNumeros = DBHandler.listaGlobalNumero
        listaFechas = DBHandler.listaGlobalFecha
        
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

        graph = pygal.Line()
        #graph = pygal.Bar()
        graph.title = 'Grafo ' + dbname
        graph.x_labels = listaFechas
        graph.add('Numeros Aleatorios', listaNumeros)
        graph_data = graph.render() 

        #print graph_data

        titulo = "Grafo " + dbname

        html = """ <html>
        <head>
        <title>%s</title>
        </head>
        <body>
        %s
        </body>
        </html>
        """ % (titulo, graph_data)

        return graph_data


#---------------------------------------------
@app.route('/')
def pygalexample():
    try:

        #Prueba---
        #listas con datos de prueba
        listaNumeros=[None] * 10
        listaFechas=[None] * 10
        for i in xrange(10):
            print "i in xrange(10): " + str(i)
            listaNumeros[i]=random.randint(0,100)
            if i == 0:
                listaFechas[i]=2000000
            else:
                listaFechas[i]=listaFechas[i-1]+random.randint(0,10000)
        

        listaNumeros.append(77)
        listaFechas.append(2100000)
        listaFechas.append(2200000)
        listaFechas.append(2300000)
        listaFechas.append(2400000)
        listaFechas.append(2500000)

        print "listaNumeros" + str(listaNumeros)
        print "listaFechas" + str(listaFechas)

        longitud = len(listaNumeros)
        print "Num\tFecha"
        for i in xrange(longitud):
            try:
                print str(listaNumeros[i]) + "\t" + str(listaFechas[i])
            except:
                print "out of range"
        

        #---

        graph = pygal.Line()
        #graph = pygal.Bar()
        graph.title = 'Test Graph'
        graph.x_labels = listaFechas
        graph.add('Numero', listaNumeros)
        graph_data = graph.render() 

        #print graph_data

        titulo = "titulo Custom"

        html = """ <html>
        <head>
        <title>%s</title>
        </head>
        <body>
        %s
        </body>
        </html>
        """ % (titulo,graph_data)

        return html
    
    except Exception, e:
        print "ERROR"
        return(str(e))

if __name__ == '__main__':    
    app.run()
