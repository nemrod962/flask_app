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

def getDatetimeMs():
    return time.time() * 1000.0

def msToDatetime(tiempoMs):
    fechabuena = datetime.datetime.fromtimestamp(tiempoMs/1000.0)
    return fechabuena

