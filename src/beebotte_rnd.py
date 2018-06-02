# -*- coding: utf-8 -*-
"""
INSERTAMOS LOS NUEMRO ALEATORIOS OBTENIDOS
DE LA WEB EN LA BASE DE DATOS DE BEEBOTTE.
"""
#include beebotte SDK for python
#from beebotte import *
from beebotte_base import BeeBasic

#Interfaz para los manejadores de bases de datos
#para trabajar con los numeros aleatorios
from interface_rnd import HandlerInterface

#expresiones regulares para parsear los datos obtenidos
import re

#logging
import logging
from log_handler import setup_log

#importamos la clase para obtener los numeros aleatorios
import web_fetcher.rnd_fetcher

class BeeHandler(BeeBasic, HandlerInterface):
    
    """
    #VARIABLES GLOBALES (de clase)
    #lista temporal con todas las entradas de beebotte (fecha)
    listaGlobalFecha = list()
    #lista temporal con todas las entradas de beebotte (numeros)
    listaGlobalNumero = list()
    """
    
    #Inicializo las variables globales en el contructor
    def __init__(self,canal="NumberList",recurso="numero"):
        BeeBasic.__init__(self, canal, recurso)
        HandlerInterface.__init__(self)
        """
        #Ya se inicializan en el contructor de HandlerInterface
        #lista temporal con todas las entradas de beebotte (fecha)
        self.listaGlobalFecha = list()
        #lista temporal con todas las entradas de beebotte (numeros)
        self.listaGlobalNumero = list()
        """

    """
        Extracción de los datos en las cadenas
        obtenidas al preguntar al servidor.
    """
    #Sacar la fecha del tiempo obtenido de toda la string obtenida
    #utilizar expresiones regulares.
    #ejemplod de la info obtenida.
    #{u'_id': u'5a2fd04c0e4d72e331909666', u'data': 82.28, u'ts': 1513082955796L, u'wts': 1513082956160L}
    def parseDate(self, cadena):
        fechaMs = re.findall('u\'ts\': (.*?),', cadena)
        #logging.debug("FECHA ANTES PARSE: " + fechaMs[0])
        #Problemas al parsear. A veces la fecha incluye la L al final 
        #y otras no. Comprobaremos si tiene L, y si es asi la quitamos.
        if fechaMs[0].endswith("L"):
            fechaMs[0]=fechaMs[0].replace("L","")
        #logging.debug("FECHA DESPUES PARSE: " + fechaMs[0])
        return fechaMs[0]

    #saca el numero de toda la string obtenida de beebotte
    def parseNumber(self, cadena):
        numero = re.findall('u\'data\': (.*?),', cadena)
        #logging.debug(numero[0])
        return numero[0]

#-------------------------------------------------------------------------
    """
    Funciones para leer y escribir especificamente los numeros aleatorios
    a la base de datos online.
    """
    #Ahora escribimos el numero aleatorio en la base de datos.
    #Devuelve 0 si se ha realizado satisfactoriamente, 1 si no.
    #BeeBotte almacena la fecha automaticamente, no hace falta
    #que tengamos otro recurso almacenandola.
    def writeRandom(self, rndNumber, debug=False):
        #comrpobamos conexion con la base de datos online
        self.checkConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("writeRandom - ModoFallo : " + str(self.sinConexion))
        if self.sinConexion == False:
            #obtenemos numero aleatorio de internet
            #rndClass = web_fetcher.rnd_fetcher.Rnd_fetcher()
            #rndNumber = rndClass.get_web_rnd()
            if debug:
                logging.debug("El numero aleatorio es: "+str(rndNumber))
            #escribimos el numero random en la BBDD online
            #es necseraio convertirlo a string para pasarlo como parametro
            success=self.writeData(self.canal,self.recurso,rndNumber,debug)
            if success == 0:
                if debug:
                    logging.debug("Numero "+str(rndNumber)+
                    " escrito satisfactoriamente en NumberList")
                return 0
            else:
                if debug:
                    logging.warning("ERROR: no se pudo escribir el numero rnd."
                    +" - cod. error" + str(success))
                    logging
                return 1
        else:
            #No hay conexion
            return 1


    #ACTUALIZO LAS LISTAS LOCALES CON LOS DATOS DE LA BD
    #Lee los numeros aleatorios ya esxitentes en la Base de datos online
    def readRandom(self, debug = False):
        #comprobamos ocnexion von Beebotte.
        self.checkConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("readRandom - ModoFallo : " + str(self.sinConexion))
        if self.sinConexion == False:
            #tengo una lista con los numeros aleatorios y su fecha en resultado
            #   #NumberList : canal (tabla de la BBDD) a utilizar
            #   #numero : variable del canal a leer
            #   #1024 : numero máximo de valores a leer
            resultado = self.readData(self.canal, self.recurso, 1024, debug)
            
            #Una vez obtenido el resultado, parsearemos y volcaremos los
            #numeros y sus fechas en dos listas de esta clase con la
            #que trabajaremos mas adelante.

            #en l tengo la longitud de la lista de los resultados
            l = len(resultado)
            #lista temporal con todas las entradas de beebotte (fecha)
            self.listaGlobalFecha = [None] * l
            #lista temporal con todas las entradas de beebotte (numeros)
            self.listaGlobalNumero = [None] * l
            if debug:
                logging.debug("LONGITUD RESULTADO: "+str(l))
            for index in xrange( l ):
                #parseo fecha
                fechaMs=self.parseDate(str(resultado[index]))
                numero =self.parseNumber(str(resultado[index]))
                #Añado a las listas globales.
                #Como mas adelante tendre que trabajar con estos
                #datos comparandolos unos con otros, los almacenaré como dato
                #numerico.

                #Fecha es un entero, pues esta en ms y no tiene decimales
                self.listaGlobalFecha[index] = int(fechaMs)
                #Numero sera un float pues tiene decimales
                self.listaGlobalNumero[index] = float(numero)
                if debug:
                    logging.debug("Entrada ["+str(index)+"] num: "+numero+
                    " fecha: "+fechaMs)
            if debug:        
                logging.debug("Todas las entradas de Beebotte")
                logging.debug(self.listaGlobalFecha)
                logging.debug(self.listaGlobalNumero)


    #Reiniciar canal de los numeros aleatorios.

#-------------------------------------------------------------------------
    #INTERFAZ DE USUARIO
    #permite al usuario añadir canales y variables a los mismos
    def user_op(self):
        repetir = True
        bclient = self.initConn()
        debug_str = raw_input("Activar Modo Debug?[Y\N]: ")
        if debug_str == "Y" or debug_str == "y":
            debug = True
        else:
            debug = False


        #Bucle principal
        while repetir:
            opcion = raw_input("Selecciona operacion:\n1.Añadir canal.\n2.Añadir variable a canal ya existente.\n3.Borrar canal.\n4.Escribir numero aleatorio.\n5.Ver numeros aleatorios.\n6.Mostrar lista numeros y tiempo.\n")
            #Añadir canal
            if opcion == "1":
                nombre = raw_input("Nombre canal: ")
                label = raw_input("Label: ")
                descr = raw_input("Descripcion: ")
                varName = raw_input("Nombre variable: ")
                varType = raw_input("Tipo variable (\"string\" o \"number\": ")
                isPublic = True
                res = self.createChannel(nombre, varName, varType, label, descr, isPublic, debug)
                logging.debug(res)
            #Añadir variable
            elif opcion == "2":
                canal = raw_input("Canal: ")
                nombre= raw_input("nombre variable: ")
                tipo= raw_input("tipo (string o number): ")
                label= raw_input("label: ")
                descr= raw_input("descripcion: ")
                sendOnSubs = False
                res = self.createResource(canal, nombre,tipo,label, descr, sendOnSubs, debug)
                logging.debug(res)
            elif opcion == "3":
                nombre = raw_input("Nombre canal: ")
                try:
                    self.deleteChannel(nombre)
                except:
                    logging.warning("No se pudo borrar canal "+nombre)
            elif opcion == "4":
                #rndClass = web_fetcher.rnd_fetcher.Rnd_fetcher()
                #rndNumber = rndClass.get_web_rnd()
                numero = web_fetcher.rnd_fetcher.Rnd_fetcher().get_web_rnd()
                self.writeRandom(numero, debug)
            elif opcion == "5":
                self.readRandom(debug)
            elif opcion == "6":
                logging.debug("Lista fechas: ")
                logging.debug(self.listaGlobalFecha)
                logging.debug("Lista numeros: ")
                logging.debug(self.listaGlobalNumero)
            #opcion no valida
            else:
                logging.debug("opcion no valida")
            
            #continuamos con el bucle
            opcion2 = raw_input("Quiere realizar otra operacion? Y/N: ")
            if(opcion2 != "Y" and opcion2 != "y"):
                repetir = False


if __name__ == "__main__":
    #Setup log
    setup_log()
    logging.warning("Iniciado!")
    #clase = BeeHandler()
    #clase.user_op()
    bee = BeeHandler("canal01","res01")
