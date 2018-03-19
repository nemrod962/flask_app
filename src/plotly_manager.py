# -*- coding: UTF-8 -*-
#PLOTLY
import plotly
import plotly.plotly as py
from plotly.graph_objs import *
#nombre de la base de datos utilizada
import web_functions
#formato y conversion fechas
import date_handler
 
"""
Clase encargada de crear grafos plot.ly con los 
datos contenidos en las bases de datos sobre
los numeros aleatorios.

Recibiremos las listas con los valores de los numeros 
y sus fechas de obtencion. Se las enviaremos a plot.ly
Para generar gráficas con ellas.

"""
class PlotlyHandler:

    def cargarCredenciales(self):
        #Abro fichero con las credenciales
        credentialsFile=open("./credentials/plotly_credentials", "r")
        myUsername=credentialsFile.readline().rstrip()
        myApiKey=credentialsFile.readline().rstrip()

        #Cargo credenciales para utlizar Plotly. Crea fichero ~/.plotly/.credentials
        plotly.tools.set_credentials_file(username=myUsername, api_key=myApiKey)

    #Doy formato a las listas en caso de estar utilizando
    #Beebotte, ya que me devuelve las listas con el orden
    #invertido.
    def formatoListas(self, DBHandler, listaNumeros, listaFechas):
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
    
    #Crea un grafo plot.ly con las listas 
    #de numeros y fechas proporcionadas.
    #Las listas las obtenemos de DBHandler,
    #que sera una instancia de SQLHandler
    #o de BeeHandler. Ambas clases contienen
    #las listas listaGlobalNumero y
    #listaGlobalFecha.
    #Accesibles mediante DBHandler.listaGlobal...
    def crearGrafo(self, DBHandler, tipo=None):
        #Cargo Credenciales para usar plot.ly
        self.cargarCredenciales()

        #Obtengo las listas de los numeros y su tiempo de obtencion
        #---
        #Aqui no obtengo una copia, si no que referencio a las mismas listas.
        #listaNumeros = DBHandler.listaGlobalNumero
        #listaFechas = DBHandler.listaGlobalFecha
        #---
        #De esta forma obtengo una copia de las listas.
        #Así puedo operar con ellas y transformarlas de forma
        #que no afecten a otras partes del programa.
        listaNumeros = list(DBHandler.listaGlobalNumero)
        listaFechas = list(DBHandler.listaGlobalFecha)

        #Doy formato a las listas.
        self.formatoListas(DBHandler, listaNumeros, listaFechas)

        #LLegados a este punto, tengo en las listas
        # listaNumeros y listaFechas los datos que
        #necesita plot.ly para crear las gráficas.

        #Le doy el formato que precisa plot.ly
        traza0 = Scatter(
            x=listaFechas,
            y=listaNumeros
        )
        
        #Puedo incluir más de una traza
        datos=Data([traza0])

    
        #envio datos a plot.ly para que genere la gráfica online.
        #En caso de no haber conexión a internet, genero la gráfica de
        #forma local
        try:
            py.plot(datos, filename="Num. aleatorios")
        except:
            print "plot.ly OFFLINE"
            #Obtengo que DB estoy empleando
            dbname = web_functions.getDBSimpleName(DBHandler)
            plotly.offline.plot({
                "data": [Scatter(x=listaFechas, y=listaNumeros)],
                "layout": Layout(title="plot.ly " + dbname)
                })