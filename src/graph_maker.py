from flask import Flask
import pygal
from pygal.style import DarkSolarizedStyle
import random
 
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
    #de numeros y fechas proporcionadas
    def grafoLineas(self, listaNumeros, listaFechas):

        graph = pygal.Line()
        #graph = pygal.Bar()
        graph.title = 'Grafo numeros aleatorios'
        graph.x_labels = listaFechas
        graph.add('Numero Aleatorio', listaNumeros)
        graph_data = graph.render() 

        #print graph_data

        titulo = "titulo"

        html = """ <html>
        <head>
        <title>%s</title>
        </head>
        <body>
        %s
        </body>
        </html>
        """ % (titulo, graph_data)

        return html


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
