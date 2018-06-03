# -*- coding: UTF-8 -*-
import random
import plotly
import plotly.plotly as py
from plotly.graph_objs import *

#Ver version Plot.ly
print plotly.__version__

#Abro fichero con las credenciales
credentialsFile=open("../credentials/plotly_credentials", "r")
myUsername=credentialsFile.readline().rstrip()
myApiKey=credentialsFile.readline().rstrip()
print "User: " + str(myUsername)
print "Api: " + str(myApiKey)

#Cargo credenciales para utilziar Plotly. Crea fichero ~/.plotly/.credentials
plotly.tools.set_credentials_file(username=myUsername, api_key=myApiKey)

#-----GRAFICA-ONLINE
#DATOS GRAFICA
#Prueba---
#listas con datos de prueba
listaNumeros=[None] * 10
listaFechas=[None] * 10
for i in xrange(10):
    listaNumeros[i]=random.randint(0,100)
    if i == 0:
        listaFechas[i]=2000000
    else:
        listaFechas[i]=listaFechas[i-1]+random.randint(0,10000)
listaNumeros.append(77)
#listaFechas.append(2999999)
print "Datos: "
print listaNumeros
print listaFechas
#Creo datos para la gŕafica Plotly
trace0 = Scatter(
        x=listaFechas,
        y=listaNumeros
        )
data = Data([trace0])

#Creo gŕafica
try:
    py.plot(data, filename = 'basic-line')
except:
    #-----GRAFICA-OFFLINE
    print "OFFLINE: "
    plotly.offline.plot({
        #"data": [Scatter(x=[1, 2, 3 ,4], y=[4, 3, 2, 1])],
        "data": [Scatter(x=listaFechas, y=listaNumeros)],
    "layout": Layout(title="prueba offline")
    })
