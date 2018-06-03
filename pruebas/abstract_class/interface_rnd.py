# -*- coding: UTF-8 -*-
"""
    Clase abstracta (interfaz) que contiene los 
    métodos que debe contener cualquier clase 
    dedicada a manejar la lectura y escritura en las bases de
    datos.
"""
from abc import ABCMeta, abstractmethod

class HandlerInterface:
    #Para que la clase sea abstracta
    __metaclass__ = ABCMeta

    def __init__(self):
        #Tendré dos listas globales donde almacenaré todos los números
        #y las fechas temporalmente, durante el tiempo de ejecución.
        self.listaGlobalNumero = list()
        self.listaGlobalFecha = list()

    
    #Metodo abstracto que el heredero deberá implementar
    @abstractmethod
    def readRandom(self):
        """Leer datos de las bases de datos
        y actualizar listas globales con ellos"""

    #Metodo abstracto que el heredero deberá implementar
    @abstractmethod
    def writeRandom(self):
        """Escribe número aleatorio en la bases de datos."""


    #Metodo abstracto que el heredero deberá implementar
    def reload(self):
        """Llamada a readRandom(). Se 
        empleará cuando se quieran actualizar las
        listas globales."""
        self.readRandom()
