# -*- coding: utf-8 -*-
"""
INSERTAMOS LOS NUEMRO ALEATORIOS OBTENIDOS
DE LA WEB EN LA BASE DE DATOS DE BEEBOTTE
TAMBIEN APORTA FUNCIONALIDAD PARA TRABAJAR CON
BEEBOTTE
"""
#include beebotte SDK for python
from beebotte import *

#expresiones regulares para parsear losd atos obtenidos
import re

#importamos la clase para obtener los numeros aleatorios
import web_fetcher.rnd_fetcher

class BeeHandler:
    
    """
    #VARIABLES GLOBALES (de clase)
    #lista temporal con todas las entradas de beebotte (fecha)
    listaGlobalFecha = list()
    #lista temporal con todas las entradas de beebotte (numeros)
    listaGlobalNumero = list()
    """
    
    #Inicializo las variables globales en el contructor
    def __init__(self):
        #lista temporal con todas las entradas de beebotte (fecha)
        self.listaGlobalFecha = list()
        #lista temporal con todas las entradas de beebotte (numeros)
        self.listaGlobalNumero = list()
    

    #Iniciamos la conexion con Beebotte
    def initConn(self):
        #bclient = BBT("API_KEY", "SECRET_KEY")
        _accesskey = "6dcd5477c26e32e1819f487f169f2a45"
        _secretkey = "e6912a135c4da71e9b2d605046f534be154d06f32ac5784f53a562ccb48d336b"
        _hostname = "api.beebotte.com"
        bclient = BBT(_accesskey, _secretkey, hostname = _hostname)
        return bclient


#-------------------------------------------------------------------------
    """
    OPTIONAL FUNCTIONS. Funciones extra que no son relevantes para el programa.
    Permiten añadir canales y recursos a la base de datos online, pero tambien
    puede hacerse desde el navegador sin la necesidad de hacerlo desde aqui
    """
    #create channel. Es necesario crear una variable tambien
    def createChannel(self, bclient, channelName, 
                    #parametros de la varable
                    varName, varType="string",
                    #parametros canal
                    myLabel="channel label", 
                    descr="channel description", isPublic=True,
                    ):
        try:
            if varType == "string":
                bclient.addChannel(
                    channelName,
                    label = myLabel,
                    description = descr,
                    ispublic = isPublic,
                    
                    resources = [
                    {
                    
                        "name": varName,
                        "vtype": BBT_Types.String
                    
                    } 
                    ]
                    
                )
            else:
                bclient.addChannel(
                    channelName,
                    label = myLabel,
                    description = descr,
                    ispublic = isPublic,
                    
                    resources = [
                    {
                    
                        "name": varName,
                        "vtype": BBT_Types.Number
                    
                    } 
                    ]
                    
                )
            return 0
        except:
            print "Error when creating channel "+channelName
            return 1

        
    #add resource
    #el canal debe existir
    #los tipos de la variable puede ser "string" o "number"
    def createResource(self, bclient, myChannel, varName, varType="string",
                        myLabel = "label", descr = "description",
                        isSendOnSubscribe=False):
        if varType == "string":
            try:
                bclient.addResource(
                    channel = myChannel,
                    name = varName,
                    vtype = BBT_Types.String,
                    label = myLabel,
                    description = descr,
                    sendOnSubscribe = isSendOnSubscribe
                )
                return 2
            except:
                print "Error adding resource "+varName
                return 1
        else:
            try:
                bclient.addResource(
                    channel = myChannel,
                    name = varName,
                    vtype = BBT_Types.Number,
                    label = myLabel,
                    description = descr,
                    sendOnSubscribe = isSendOnSubscribe
                )
                return 0
            except :
                print "Error adding resource "+varName
                return 1

#-------------------------------------------------------------------------
    """
    Funciones para escribir y leer datos de la base de datos online
    """
    #WRITE DATA
    def writeData(self, bclient, channel, varName, value, debug = False):
        try:
            #Create a Resource object
            res = Resource(bclient, channel, varName)
            #write to the resource
            res.write(value)
            return 0
            
        except:
            if debug:
                print "Could not write value "+value+" into variable "+varName
            return 1
        

    #READ DATA
    def readData(self, bclient, channel, varName, myLimit = 5, debug = False):
        #read resources
        records = bclient.read(channel, varName, myLimit)
        if debug:
            print "Estoy leyendo."
            for x in records:
                print x
        return records

    #sacar la fecha del tiempo obtenido de toda la string obtenida
    #utilizar expresiones regulares.
    #ejemplod de la info obtenida.
    #{u'_id': u'5a2fd04c0e4d72e331909666', u'data': 82.28, u'ts': 1513082955796L, u'wts': 1513082956160L}
    def parseDate(self, cadena):
        fechaMs = re.findall('u\'ts\': (.*?)L', cadena)
        #print fechaMs[0]
        return fechaMs[0]

    #saca el numero de toda la string obtenida de beebotte
    def parseNumber(self, cadena):
        numero = re.findall('u\'data\': (.*?),', cadena)
        #print numero[0]
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
        #iniciamos conexion con la base ded datos online
        bclient = self.initConn()
        #obtenemos numero aleatorio de internet
        #rndClass = web_fetcher.rnd_fetcher.Rnd_fetcher()
        #rndNumber = rndClass.get_web_rnd()
        if debug:
            print "El numero aleatorio es: "+str(rndNumber)
        #escribimos el numero random en la BBDD online
        #es necseraio convertirlo a string para pasarlo como parametro
        success=self.writeData(bclient,"NumberList","numero",rndNumber,debug)
        if success == 0:
            if debug:
                print "Numero "+str(rndNumber)+" escrito satisfactoriamente en NumberList"
            return 0
        else:
            if debug:
                print "ERROR: no se pudo escribir el numero "+str(rndNumber)
            return 1
    
    #Lee los numeros aleatorios ya esxitentes en la Base de datos online
    def readRandom(self, debug = False):
        bclient = self.initConn()
        #tengo una lista con los numeros aleatorios y su fecha en resultado
        resultado = self.readData(bclient, "NumberList", "numero", 1024, debug)
        
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
            print "LONGITUD RESULTADO: "+str(l)
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
                print "Entada ["+str(index)+"] num: "+numero+" fecha: "+fechaMs
        if debug:        
            print "Todas las entradas de Beebotte"
            print self.listaGlobalFecha
            print self.listaGlobalNumero

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
                res = createChannel(bclient, nombre, varName, varType, label, descr)
                print res
            #Añadir variable
            elif opcion == "2":
                canal = raw_input("Canal: ")
                nombre= raw_input("nombre variable: ")
                tipo= raw_input("tipo (string o number): ")
                label= raw_input("label: ")
                descr= raw_input("descripcion: ")
                res = createResource(bclient, canal, nombre,tipo,label, descr)
                print res
            elif opcion == "3":
                nombre = raw_input("Nombre canal: ")
                try:
                    bclient.deleteChannel(nombre)
                except:
                    print "No se pudo borrar canal "+nombre
            elif opcion == "4":
                #rndClass = web_fetcher.rnd_fetcher.Rnd_fetcher()
                #rndNumber = rndClass.get_web_rnd()
                numero = web_fetcher.rnd_fetcher.Rnd_fetcher().get_web_rnd()
                self.writeRandom(numero, debug)
            elif opcion == "5":
                self.readRandom(debug)
            elif opcion == "6":
                print "Lista fechas: "
                print self.listaGlobalFecha
                print "Lista numeros: "
                print self.listaGlobalNumero
            #opcion no valida
            else:
                print "opcion no valida"
            
            #continuamos con el bucle
            opcion2 = raw_input("Quiere realizar otra operacion? Y/N: ")
            if(opcion2 != "Y" and opcion2 != "y"):
                repetir = False

if __name__ == "__main__":
    clase = BeeHandler()
    clase.user_op()
