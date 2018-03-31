# -*- coding: utf-8 -*-
"""
Clase encargada de almacenar los números
aleatorios y su tiempo de obtención en
MongoDB.

Hereda de la clase MongoBasic que se 
encuentra en el archivo mongo_base.py

La base de datos a emplear viene indicada
en el archivo de credenciales ('mydb').

La colección en la que escribiremos los números 
será 'NumberList'.

Los nombres de los campos en los documentos
serán "numero" para los números y
"fecha" para las fechas
"""
#Clase padre
from mongo_base import MongoBasic
#Manejo de fechas
import date_handler

class MongoHandler(MongoBasic):
    """
     ____        _ _     _ 
    | __ ) _   _(_) | __| |
    |  _ \| | | | | |/ _` |
    | |_) | |_| | | | (_| |
    |____/ \__,_|_|_|\__,_|

    """
    
    #Constructor
    #Inicializo las variables.
    def __init__(self, coleccion="NumberList", limite=1024, debug=False):
        MongoBasic.__init__(self,coleccion,limite,debug)
        #para mensajes de debug
        self.debug=debug
        #Tendré dos listas globales donde almacenaré todos los números
        #y las fechas temporalmente, durante el tiempo de ejecución.
        self.listaGlobalNumero = list()
        self.listaGlobalFecha = list()
        #Nombres de los campos en los que se escribirán los 
        #números y las fechas
        self.campoNumero="numero"
        self.campoFecha="fecha"
        #self.campoNumero="var1"
        #self.campoFecha="var2"

    #Cerrar conexion con MongoDB
    def close(self):
        self.endConn()

        """
         ____                _ 
        |  _ \ ___  __ _  __| |
        | |_) / _ \/ _` |/ _` |
        |  _ <  __/ (_| | (_| |
        |_| \_\___|\__,_|\__,_|

        """

    def readRandom(self):
        #Obtendremos los datos ordenados por el tiempo, de 
        #más a menos recientes, de forma que si se llega al
        #limite de documentos devueltos se obtengan los datos
        #más recientes
        
        res = self.leerOrden(self.campoFecha,False)

        if res==None:
            if self.debug:
                print "No hay conexion con MongoDB."
        else:
            #Limpio listas antes de almacenar los 
            #nuevos datos
            self.listaGlobalNumero = list()
            self.listaGlobalFecha = list()
            #Almaceno los resultados en las listas:
            for doc in res:
                fechaActual = doc[self.campoFecha]
                numeroActual = doc[self.campoNumero]
                #Añado a las listas 
                self.listaGlobalNumero.append(numeroActual)
                self.listaGlobalFecha.append(fechaActual)

            if self.debug:
                "MONGODB - Numeros:"
                print self.listaGlobalNumero
                "MONGODB - Fechas:"
                print self.listaGlobalFecha


if __name__ == "__main__":
    c = MongoHandler()
    c.debug=True
    c.setColeccion("test")
    c.readRandom()
