# -*- coding: UTF-8 -*-

"""
Esta clase se encargara de subir
los números aleatorios y su fecha 
tanto a la base de datos MySQL local
como a Beebotte cada dos minutos
"""

#Process para crear procesos. la variable enable deberá ser
#del tipo Value para que su valor se comparta entre procesos
from multiprocessing import Process, Value
#para esperar los dos minutos
import time
#librerias propias para trabajar con las bases de datos
import sql_rnd
import beebotte_rnd
#libreria propia para extraer un numero aleatorio de la web
import web_fetcher.rnd_fetcher
#libreria propia para trabajar con las fechas
import date_handler

class RndUploader:

    #Esta clase tiene un único atributo que es enable y
    #se inicializa como True. Miestras tenga este valor
    #se seguiran subiendo datos cada 2 minutos.
    #cuando se cambie su valor a Flase parara.
    def __init__(self, flaskApp, handSQL, handBee,\
    tiempoSleep = 120, debug = False):
        #self.__enable -> __enable es privado gracias a '__'
        #para acceder al valor de enable utilizaremos
        #self.__enable.value
        self.__enable=Value('b', True)
        #modo debug
        self.__debug=debug
        #tiempo a esperar entre inserciones
        self.__tiempo = tiempoSleep
        #Creo instancias PRIVADAS de las clases a utilizar
        #para obtener los  numeros aleatorios
        self.__RndGen = web_fetcher.rnd_fetcher.Rnd_fetcher()
        #manejar BBDD
        #self.__SQLHand = sql_rnd.SQLHandler(flaskApp)
        #self.__BeeHand = beebotte_rnd.BeeHandler()
        self.__SQLHand = handSQL
        self.__BeeHand = handBee
        #inicio proceso para subir los datos a las BBDD
        self.lanzar()
    
    #Devuelve el manejador de MySQL
    def getSQLHandler(self):
        return self.__SQLHand

    #Devuelve el manejador de Beebotte
    def getBeeHandler(self):
        return self.__BeeHand
    
    #Subira un número aleatorio cada 2 min
    def upload(self):
        while self.__enable.value:

            #obtenemos numero aleatorio a insertar
            rnd = self.__RndGen.get_web_rnd()

            if self.__debug:
                print "num aleatorio a escribir: " + str(rnd)

            
            #BORRA ESTO!-----------------------------
            print "PELIGRO: BORRA ESTO!!! rnd-uploader.upload() line-70"
            self.__enable.value = False
            self.__SQLHand.readDataDB()
            self.__BeeHand.readRandom()
            #BORRA ESTO!-----------------------------
            

            #Escribir
            if(self.__enable.value):
                #escribo en Beebotte
                self.__BeeHand.writeRandom(rnd, self.__debug)
                #solo necesario para la BD local, ya que Beebotte
                #almacena automaticamente la fecha
                fecha = str(date_handler.getDatetimeMs())
                #escribo en MySQL
                self.__SQLHand.writeDataDB(rnd, fecha, self.__debug)
                
                #ACTUALIZO LOS DATOS EN LAS LISTAS LOCALES 
                #DE LOS MANEJADORES
                self.__SQLHand.readDataDB()
                self.__BeeHand.readRandom()
                
                if self.__debug:
                    print "Tablas MySQL:"
                    print self.__SQLHand.listaGlobalFecha
                    print self.__SQLHand.listaGlobalNumero
                    print "Tablas Bee:"
                    print self.__BeeHand.listaGlobalFecha
                    print self.__BeeHand.listaGlobalNumero

                #esperar entre escrituras
                try:
                    time.sleep(self.__tiempo)
                except:
                    if self.__debug:
                        print "Uploader.upload(): sleep interrumpido!"

        print "Uploader.upload(): saliendo..."
    
    #funcion utilizada para testing
    def hola(self, nombre):
        while self.__enable.value:
            print "hola " + nombre + " "+ str(self.__enable.value)
            try:
                time.sleep(5)
            except:
                print "Uploader.hola(): sleep fue interrumpido!"
                #self.__enable.value = False
        print "Uploader.hola(): PROCESO ACABADO"

    #funcion de prueba para probar el multiprocesamiento
    #genera el proceso
    def lanzar(self):
        #proceso que será el uploader.
        #si solo pasamos un parametro como argumento (args),
        #tendremos que poner una coma detras de el, que es la
        #forma de decir que es una tupla de un solo elemento.
        #Sin esta coma (',') la creación del proceso falla
        #self.proceso = Process(target=self.upload, args=(self.__debug,) )
        self.proceso = Process(target=self.upload)
        #inicio proceso
        self.proceso.start()
        #proceso.join()

    def finalizar(self):
        self.__enable.value=False
        if self.__debug:
            print "Bandera activada para finalizar: " + str(self.__enable.value)
            print "Esperando para acabar"
        self.proceso.join()
        if self.__debug:
            print "el proceso ya ha acabado"

if __name__ == '__main__':
    print "Has ejecutado rnd_uploader.py"
    #clase = RndUploader(10, True)
    #clase.__enable.value=False
    #clase.finalizar()
