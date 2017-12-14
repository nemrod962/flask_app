# -*- coding: UTF-8 -*-

"""
Esta clase se encargara de subir
los números aleatorios y su fecha 
tanto a la base de datos MySQL local
como a Beebotte cada dos minutos
"""

#para crear procesos
import multiprocessing
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
    def __init__(self, tiempoSleep = 120, debug = False):
        #self.__enable -> __enable es privado gracias a '__'
        self.enable=True
        #modo debug
        self.__debug=debug
        #tiempo a esperar entre inserciones
        self.__tiempo = tiempoSleep
        #Creo instancias PRIVADAS de las clases a utilizar
        #para obtener los  numeros aleatorios
        self.__RndGen = web_fetcher.rnd_fetcher.Rnd_fetcher()
        #manejar BD local
        self.__SQLHand = sql_rnd.SQLHandler()
        self.__BeeHand = beebotte_rnd.BeeHandler()
        #inicio proceso para subir los datos a las BBDD
        self.upload(self.__debug)
    
    #Subira un número aleatorio cada 2 min
    def upload(self, debug=False):
        while self.enable:

            #obtenemos numero aleatorio a insertar
            rnd = self.__RndGen.get_web_rnd()

            if debug:
                print "num aleatorio a escribir: " + str(rnd)
            
            #Escribir
            if(self.enable):
                self.__BeeHand.writeRandom(rnd, debug)
                #solo necesario para la BD local, ya que Beebotte
                #alamcena automaticamente la fecha
                fecha = str(date_handler.getDatetimeMs())
                self.__SQLHand.writeDataDB(rnd, fecha, debug)

                if debug:
                    self.__SQLHand.readDataDB()
                    print "Tablas MySQL:"
                    print self.__SQLHand.listaGlobalFecha
                    print self.__SQLHand.listaGlobalNumero
                    self.__BeeHand.readRandom()
                    print "Tablas Bee:"
                    print self.__BeeHand.listaGlobalFecha
                    print self.__BeeHand.listaGlobalNumero

            time.sleep(self.__tiempo)

        print "UPLOADER: saliendo..."

if __name__ == '__main__':
    clase = RndUploader(10, True)
