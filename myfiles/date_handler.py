"""
FICHERO SIMPLE PARA OBTENER FECHA Y HORA
"""

import time

def getDate():
    fecha = time.strftime("%Y-%m-%d")
    return fecha


def getTime():
    hora = time.strftime("%H:%M:%S")
    return hora
