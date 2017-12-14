"""
FICHERO SIMPLE PARA OBTENER FECHA Y HORA
"""

import time
import datetime

def getDate():
    fecha = time.strftime("%Y-%m-%d")
    return fecha

def getTime():
    hora = time.strftime("%H:%M:%S")
    return hora

#time.time() deuvuelve el tiempo actual en microsegundos.
#como queremos milisegundos, nos quedaran 3 cifras decimales.
#utilizaremos int.round() para quitar los decimales
def getDatetimeMs():
    timeMs = int(round(time.time() * 1000.0))
    return timeMs

def msToDatetime(tiempoMs):
    #Redondeo para que los segundos no tengan decimales
    fechaSegundos = int(round(tiempoMs/1000.0))
    fechabuena = datetime.datetime.fromtimestamp(fechaSegundos)
    return fechabuena

