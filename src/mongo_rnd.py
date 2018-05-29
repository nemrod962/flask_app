# -*- coding: utf-8 -*-
"""
Clase encargada de almacenar los números
aleatorios y su tiempo de obtención en
MongoDB.

Hereda de la clase MongoBasic que se 
encuentra en el archivo mongo_base.py

La base de datos a emplear viene indicada
en el archivo de credenciales ('flask_db').

La colección en la que escribiremos los números 
será 'NumberList'.

Los nombres de los campos en los documentos
serán "numero" para los números y
"fecha" para las fechas
"""
#Clase padre
from mongo_base import MongoBasic
#Interfaz para los manejadores de bases de datos
#para trabajar con los numeros aleatorios
from interface_rnd import HandlerInterface
#Manejo de fechas
import date_handler
#logging
import logging
from log_handler import setup_log


class MongoHandler(MongoBasic, HandlerInterface):
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
        HandlerInterface.__init__(self)
        
        """
        #Ya se inicializan en el contructor de HandlerInterface
        #Tendré dos listas globales donde almacenaré todos los números
        #y las fechas temporalmente, durante el tiempo de ejecución.
        self.listaGlobalNumero = list()
        self.listaGlobalFecha = list()
        """
        #Nombres de los campos en los que se escribirán los 
        #números y las fechas
        self.campoNumero="numero"
        self.campoFecha="fecha"
        #self.campoNumero="var1"
        #self.campoFecha="var2"

        #para mensajes de debug
        self.debug=True

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
        #Devuelve el número de documentos leidos.
        #Se devuelve -1 en caso de error.
        res = self.leerOrden(self.campoFecha,False)

        if res==None:
            if self.debug:
                logging.debug("No hay conexion con MongoDB.")
        else:
            #Limpio listas antes de almacenar los 
            #nuevos datos
            self.listaGlobalNumero = list()
            self.listaGlobalFecha = list()
            #Almaceno los resultados en las listas:
            for doc in res:
                fechaActual = doc[self.campoFecha]
                numeroActual = doc[self.campoNumero]
                
                #Al insertar las fechas en MongoDB 
                #normalmente se les añade una 'L' 
                #al final.
                #Borraremos esta 'L' antes de meter 
                #las fechas en las lista globales.
                #La 'L' se debe a que el tipo de dato 
                #de la fecha es Int64, por lo que no 
                #hay que preocuparse, ya que se
                #considera como un entero y la funcion
                #msToDatetime() funciona correctamente.
                #if fechaActual.endswith("L"):
                #    fechaActual=fechaActual.replace("L","")
                #PRUEBA
                #temp = date_handler.msToDatetime(fechaActual)
                #logging.debug("Prueba: " + str(temp))

                #Añado a las listas 
                self.listaGlobalNumero.append(numeroActual)
                self.listaGlobalFecha.append(fechaActual)

            if self.debug:
                "MONGODB - Numeros:"
                logging.debug(self.listaGlobalNumero)
                "MONGODB - Fechas:"
                logging.debug(self.listaGlobalFecha)
        
        try:
            return res.count()
        except AttributeError:
            if self.debug:
                "readRandom - No se ha podido leer de MongoDB"
            return -1


    #INTERFAZ PARA CARGAR EN LAS LISTAS GLOBALES
    #LOS DATOS DE LAS BASES DE DATOS.
    #Este metodo se llamará igual tanto en el
    #manejador de SQL como de Beebotte como de MongoDB.
    #Ya implementado por HandlerInterface
    """
    def reload(self):
        self.readRandom()
    """


    """
    __        __    _ _       
    \ \      / / __(_) |_ ___ 
     \ \ /\ / / '__| | __/ _ \
      \ V  V /| |  | | ||  __/
       \_/\_/ |_|  |_|\__\___|

    """

    #Escribo en MongoDB el número aleatorio recibido.
    #Devuelve 0 si se han escrito los datos satisfactoriamente,
    #1 en caso contrario.
    #Si no hay conexion, se devuelve -1.
    def writeRandom(self, rndNumber, fecha):
        
        #Obtengo la fecha actual para almacenarla
        #junto con el número aleatorio
        #fechaObt = date_handler.getDatetimeMs()
        #La recibo como parámetro
        fechaObt=fecha
            
        #El método escribir() de MongoBasic recibe
        #los datos a escribir en MongoDB en forma
        #de diccionario: {"nombreVariable": valor }
        datosEscribir = { self.campoNumero : rndNumber,\
        self.campoFecha : fechaObt}

        #Escribo en MongoDB. Función de MongoBasic (padre).
        #Devuelve 0 si se han escrito los datos satisfactoriamente,
        #1 en caso contrario.
        res=self.escribir(datosEscribir)

        return res


    """
     ____       _      _       
    |  _ \  ___| | ___| |_ ___ 
    | | | |/ _ \ |/ _ \ __/ _ \
    | |_| |  __/ |  __/ ||  __/
    |____/ \___|_|\___|\__\___|

    """

    #Borra todas las entradas cuya fecha de obtención es igual
    # o anterior a la indicada.
    #La fecha debe estar en Ms. Si tiene una 'L' al final es de tipo long.
    #Devuelve 0 si se han borrado los datos satisfactoriamente,
    #1 en caso contrario.
    #Si no hay conexion, se devuelve -1.
    def deletePrevDate(self, date):
        if not isinstance(date, int) and not isinstance(date, long):
            if self.debug:
                logging.debug("Fecha indicada no valida: no es de tipo int o long: ")
                logging.debug(date)
            res = 1
        else:
            condicionBorrado = {self.campoFecha : {"$lte": date} }
            #Borro
            res = self.borrar(condicionBorrado)
        #'res' contiene 0 si se han borrado los datos, 1 si no.
        return res

    #Borra todos los datos de MongoDB en la coleccion actual.
    def deleteAll(self):
        res = self.borrar({})
        return res

if __name__ == "__main__":
    setup_log()

    c = MongoHandler()
    #c.debug=True
    #c.setColeccion("test")
    #c.readRandom()

    #RND
    from web_fetcher.rnd_fetcher import Rnd_fetcher
    rndGen = Rnd_fetcher()
    numRand = rndGen.get_web_rnd()
    logging.debug("numRand: " + str(numRand))
    fechaObt = date_handler.getDatetimeMs()
    logging.debug("fecha aprox: " + str(fechaObt))

    resw=c.writeRandom(numRand)
    logging.debug("resw: " + str(resw))

    resr=c.readRandom() 
    logging.debug("resr: " + str(resr))

    logging.debug("ListaNumeros: ")
    logging.debug(c.listaGlobalNumero)
    logging.debug("ListaFechas: ")
    logging.debug(c.listaGlobalFecha)
    
    #fechaPrev=123,2131215654
    fechaPrev=1522581148056L
    resb=c.deletePrevDate(fechaPrev)
    #resb=c.deleteAll()
    logging.debug("resb: " + str(resb))
    
    #Cierro conexion
    c.close()
