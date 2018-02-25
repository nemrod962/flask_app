# -*- coding: UTF-8 -*-
"""
FICHERO SIMPLE PARA OBTENER FECHA Y HORA
"""

import time
import datetime

#devuelve la fecha actual en formato "%Y-%m-%d"
def getDate():
    fecha = time.strftime("%Y-%m-%d")
    return fecha

#devuelve la fecha actual en formato "%H:%M:%S"
def getTime():
    hora = time.strftime("%H:%M:%S")
    return hora
 
#devuelve la fecha actual en formato "%Y-%m-%d %H:%M:%S"
def getDatetime():
    date = time.strftime("%Y-%m-%d %H:%M:%S")
    return date

#Devuleve la fecha actual en milisegundos
#time.time() deuvuelve el tiempo actual en microsegundos.
#como queremos milisegundos, nos quedaran 3 cifras decimales.
#utilizaremos int.round() para quitar los decimales
def getDatetimeMs():
    timeMs = int(round(time.time() * 1000.0))
    return timeMs

#Dada una fecha en milisegundos devuelve su equivalente
#en formato "%Y-%m-%d %H:%M:%S"
def msToDatetime(tiempoMs):
    #Redondeo para que los segundos no tengan decimales
    fechaSegundos = int(round(tiempoMs/1000.0))
    fechabuena = datetime.datetime.fromtimestamp(fechaSegundos)
    return fechabuena

#Dada una fecha en string con el formato 'año-mes-dia hora:min:seg' 
#devuelve su equivalencia en milisegundos
def datetimeToMs(fechaCadena):
    date = datetime.strptime(fechaCadena, "%Y-%m-%d %H:%M:%S").strftime('%s')
    dateMs = int(date)*1000
    return dateMs