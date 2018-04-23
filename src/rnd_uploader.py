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
import mongo_rnd
#libreria propia para extraer un numero aleatorio de la web
import web_fetcher.rnd_fetcher
#libreria propia para trabajar con las fechas
import date_handler

class RndUploader:

    #Esta clase tiene un único atributo que es enable y
    #se inicializa como True. Miestras tenga este valor
    #se seguiran subiendo datos cada 2 minutos.
    #cuando se cambie su valor a Flase parara.
    def __init__(self, flaskApp, handSQL, handBee, handMongo,\
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
        #MongoClient opened before fork. Create MongoClient only after forking.
        #See PyMongo's documentation for details:
        #http://api.mongodb.org/python/current/faq.html#is-pymongo-fork-safe
        #No es seguro que esta clase reciba la instancia de MongoDB del main
        #Por lo que creare en esta clase mi propia instancia de MongoHandler
        #Esto no debería importar ya que aunque sean dos instancias distintas
        #leerán de la misma base de datos.
        #La instancia en esta clase se dedicará principalmente a escribir y la
        #que está en el main a leer.
        #
        #Debo crearla una vez dentro del subproceso creado, es decir,
        #dentro de la función upload que es la que ejecuta el proceso.
        #self.__MongoHand= handMongo
        #self.__MongoHand= mongo_rnd.MongoHandler()
        #inicio proceso para subir los datos a las BBDD
        self.lanzar()
    
    #Devuelve el manejador de MySQL
    def getSQLHandler(self):
        return self.__SQLHand

    #Devuelve el manejador de Beebotte
    def getBeeHandler(self):
        return self.__BeeHand

    #Devuelve el manejador de MongoDB
    def getMongoHandler(self):
        return self.__MongoHand

    #Subira un número aleatorio cada 2 min
    def upload(self):
        #MongoClient opened before fork. Create MongoClient only after forking.
        #See PyMongo's documentation for details:
        #http://api.mongodb.org/python/current/faq.html#is-pymongo-fork-safe
        #No es seguro que esta clase reciba la instancia de MongoDB del main
        #Por lo que creare en esta clase mi propia instancia de MongoHandler
        #Esto no debería importar ya que aunque sean dos instancias distintas
        #leerán de la misma base de datos.
        #La instancia en esta clase se dedicará principalmente a escribir y la
        #que está en el main a leer.
        #
        #Debo crearla una vez dentro del subproceso creado, es decir,
        #dentro de la función upload que es la que ejecuta el proceso.
        self.__MongoHand= mongo_rnd.MongoHandler()

        while self.__enable.value:

            #obtenemos numero aleatorio a insertar
            rnd = self.__RndGen.get_web_rnd()

            if self.__debug:
                print "num aleatorio a escribir: " + str(rnd)

            """
            #BORRA ESTO!-----------------------------
            #Este trozo de codigo sirve para que esta
            #clase no suba numeros.
            print "PELIGRO: BORRA ESTO!!! rnd-uploader.upload() line-70"
            self.__enable.value = False
            self.__SQLHand.readDataDB()
            self.__BeeHand.readRandom()
            self.__MongoHand.readRandom()
            #BORRA ESTO!-----------------------------
            """

            #Escribir
            if(self.__enable.value):
                
                #La funcion de obtener numeros aleatorios
                #devuelve -1 en caso de no haber podido conectar
                #con la web de donde obtenemos los numeros aleatorios.
                #En este caso, rnd sera = a -1, por lo que no guardaremos
                #este valor en las BDs.
                if rnd > -1:
                    #escribo en Beebotte
                    self.__BeeHand.writeRandom(rnd, self.__debug)
                    #solo necesario para la BD local, ya que Beebotte
                    #almacena automaticamente la fecha
                    fecha = str(date_handler.getDatetimeMs())
                    #escribo en MongoDB
                    self.__MongoHand.writeRandom(rnd, fecha)
                    #escribo en MySQL
                    self.__SQLHand.writeDataDB(rnd, fecha, self.__debug)
                
                #ACTUALIZO LOS DATOS EN LAS LISTAS LOCALES 
                #DE LOS MANEJADORES
                self.__SQLHand.readDataDB()
                self.__BeeHand.readRandom()
                self.__MongoHand.readRandom()
                
                if self.__debug:
                    print "Tablas MySQL:"
                    print self.__SQLHand.listaGlobalFecha
                    print self.__SQLHand.listaGlobalNumero
                    print "Tablas Bee:"
                    print self.__BeeHand.listaGlobalFecha
                    print self.__BeeHand.listaGlobalNumero
                    print "Tablas Mongo:"
                    print self.__MongoHand.listaGlobalFecha
                    print self.__MongoHand.listaGlobalNumero

                #esperar entre escrituras
                try:
                    time.sleep(self.__tiempo)
                except:
                    if self.__debug:
                        print "Uploader.upload(): sleep interrumpido!"

        print "Uploader.upload(): saliendo..."
    

    #Función que genera un proceso que ejecuta la función
    #upload() de esta misma clase en segundo plano.
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

    #Marca y espera que los procesos en segundo plano terminen su ejecución.
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
