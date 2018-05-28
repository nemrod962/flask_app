# -*- coding: utf-8 -*-
"""
APORTA FUNCIONALIDAD BASE
PARA TRABAJAR CON BEEBOTTE.
-> CREAR CANALES Y VARIABLES.
-> ESCRIBIR Y LEER DATOS.
"""
#include beebotte SDK for python
from beebotte import *

#expresiones regulares para parsear los datos obtenidos
#import re

#logging
import logging
from log_handler import setup_log

#importamos la clase para obtener los numeros aleatorios
#import web_fetcher.rnd_fetcher

class BeeBasic:
    
    #Inicializo las variables globales en el contructor
    def __init__(self,canal="NumberList",recurso="numero"):
        
        """
		As a reminder, Beebotte resource description uses 
        a two levels hierarchy:
        -> Channel (canal) : physical or virtual connected 
        object (an application, an arduino, a coffee 
        machine, etc) providing some resources.
        -> Resource: most elementary part of Beebotte, this 
        is the actual data source (e.g. temperature 
        from a domotics sensor).

        """
        #Canal a emplear
        self.canal=canal
        #Recurso dentro del canal.
        #De él leeremos y escribiremos los datos.
        self.recurso = recurso
        """
        Modoa prueba de fallos. En caso de que no se pueda conectar
        con Beebotte, se activará este modo, de forma
        que esta clase no realizará ninguna función pero evitara el 
        crasheo de la aplicación.
        En un principio stará desactivado, pero si fallamos al conectar
        a la base da datos en la funcion initConn(), lo activamos.
        """
        self.sinConexion=False
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()

    
    #Iniciamos la conexion con Beebotte. Devuelve el cliente
    #que representa la conexión.
    def initConn(self):
        #bclient = BBT("API_KEY", "SECRET_KEY")
        #Leo las credenciales de un fichero en vez de meterlas a mano
        """
        _accesskey = "6dcd5477c26e32e1819f487f169f2a45"
        _secretkey = "e6912a135c4da71e9b2d605046f534be154d06f32ac5784f53a562ccb48d336b"
        """
        #Inicializo en caso de fallar al abrir el fichero
        _accesskey = "placeholder"
        _secretkey = "placeholder"
        #Abro fichero.
        try:
            bee_key_file=open("credentials/beebotte_credentials", "r")
            #Leo linea a linea las credenciales. Debo respetar el orden
            #en el que estan escritas las credenciales.
            #Al leer una linea, tengo '\n' al final.
            #rstrip() me elimina este caracter.
            _accesskey = bee_key_file.readline().rstrip() 
            _secretkey = bee_key_file.readline().rstrip()
            #cierro fichero
            bee_key_file.close()
        except IOError as e:
            logging.debug("Beebotte Handler: " + str(e))
            self.sinConexion=True
            logging.debug("Beebotte - Modo sin conexion: " +
            str(self.sinConexion))

        _hostname = "api.beebotte.com"
        bclient = BBT(_accesskey, _secretkey, hostname = _hostname)
        logging.debug("Conectando a Beebotte...")
        
        #COMPROBACION DE LA CONECTIVIDAD CON BEEBOTTE
        #Intento leer un valor de beebotte
        try:
            #Como estoy comprobando constantemente la conexion,
            #Empiezo suponiendo que tengo conectividad. Si no es asi,
            #cambio la variable e indico que no hay conectividad.
            #Hago esta comprobacion para que cuando pase de no tener
            #conectividad a tenerla, la variable sinConexion pase
            #a tener valor False, de forma que la funciones realmente
            #realicen sus operaciones
            self.sinConexion=False
            bclient.read(self.canal, self.recurso, 1)
        except:
            logging.warning("No se pudo conectar con Beebotte.")
            self.sinConexion=True
            logging.debug("Beebotte - Modo sin conexion: " +
            str(self.sinConexion))

        return bclient


#-------------------------------------------------------------------------
    """
    Funciones para escribir y leer datos de la base de datos online
    """
    #WRITE DATA
    def writeData(self, channel, varName, value, debug = False):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
            try:
                #Create a Resource object
                res = Resource(self.bclient, channel, varName)
                #write to the resource
                res.write(value)
                return 0
                
            except:
                logging.warning("Could not write value "+ str(value) +
                    " into variable " + str(varName))
                return 1
        else:
            #no hay conexion
            return 2
        

    #READ DATA
    def readData(self, channel, varName, myLimit = 1024, debug = False):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
            #read resources
            records = self.bclient.read(channel, varName, myLimit)
            logging.warning("IMPORTANTE: TIPO records: " + str(type(records)))
            if debug:
                logging.debug("Estoy leyendo.")
                for x in records:
                    logging.debug(x)
            return records
        else:
            #el tipo de records es list.
            #si no hay conexion devulevo lista vacia
            return list()

#-------------------------------------------------------------------------
    """
    OPTIONAL FUNCTIONS. Funciones extra que no son relevantes para el programa.
    Permiten añadir canales y recursos a la base de datos online, pero tambien
    puede hacerse desde el navegador sin la necesidad de hacerlo desde aqui
    """
    #create channel. Es necesario crear una variable tambien.
    def createChannel(self, channelName, 
                    #parametros de la varable
                    varName, varType="number",
                    #parametros canal
                    myLabel="channel label", 
                    descr="channel description", isPublic=True,
                    debug=False
                    ):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()

        if debug:
            logging.debug("createChannel - modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
            try:
                if varType == "string":
                    bclient.addChannel(
                        channelName,
                        label = myLabel,
                        description = descr,
                        ispublic = isPublic,
                        
                        resources = [ {
                            "name": varName,
                            "vtype": BBT_Types.String
                        } ]
                        
                    )
                else:
                    bclient.addChannel(
                        channelName,
                        label = myLabel,
                        description = descr,
                        ispublic = isPublic,
                        
                        resources = [ {
                            "name": varName,
                            "vtype": BBT_Types.Number
                        } ]
                    )
                return 0
            except:
                logging.warning("Error when creating channel "+channelName)
                return 1

        
    #ADD RESOURCE. Añade una 'variable' al canal.
    #El canal debe existir.
    #los tipos de la variable pueden ser "string" o "number".
    def createResource(self, myChannel, varName, varType="number",
                        myLabel = "label", descr = "description",
                        isSendOnSubscribe=False, debug=False):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("createResource - modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
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
                    logging.warning("Error adding resource "+varName)
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
                    logging.warning("Error adding resource "+varName)
                    return 1

    #REMOVE CHANNEL
    def deleteChannel(self, channel):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
            logging.debu("Borrando canal: " + str(channel))
            return self.bclient.deleteChannel(str(channel))
        

    #REMOVE RESOURCE
    def deleteResource(self, channel, resource):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
            logging.debu("Borrando recurso: " + str(resource)
            + " del canal: " + str(channel))
            return self.bclient.deleteChannel(str(channel), str(resource))

    #RESET CHANNEL
    def resetChannel(self, channel, myLabel="channel label",\
    descr="channel description", isPublic=True,debug=False):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
            #Guardo info recurso (nombre y tipo). El del canal ya lo tengo.
            varName = self.getResourceName(channel)
            varType = self.getResourceType(channel)
            logging.info("Nombre Res: " + str(varName))
            logging.info("Tipo Res: " + str(varType))
            #Borro canal
            self.deleteChannel(channel)
            #lo vuelvo a crear
            self.createChannel(channel,varName,varType,myLabel,\
            descr, isPublic, debug)

    #RESET RESOURCE
    def resetResource(self, channel, varName=None, varType=None,\
    myLabel="channel label", descr="channel description",\
    sendOnSubs=False, debug=False):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
            #Guardo info recurso (nombre y tipo). El del canal ya lo tengo.
            if varName == None:
                varName = self.getResourceName(channel)
            if varType == None:
                varType = self.getResourceType(channel)
            logging.info("Nombre Res: " + str(varName))
            logging.info("Tipo Res: " + str(varType))
            #Borro canal
            self.deleteResource(channel, varName)
            #lo vuelvo a crear
            self.createResource(channel,varName,varType,myLabel,\
            descr, sendOnSubs, debug)

    #Devuelve nombre del canal indicado
    def getChannelName(self, channel=None):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        logging.debug("modo sin conexion : " + str(self.sinConexion))
        if self.sinConexion == False:
            if channel == None:
                channel = self.canal
        #datos es de tipo dict()
        """
        {u'description': u'lista con numeros aleatorios', u'ispublic': True,
        u'label': u'label', u'token': u'1513081905125_RP02tuBl9e4HvVTH',
        u'owner': u'nemrod962', u'creationTimestamp': 1513081905127, u'id':
        u'nemrod962.NumberList', u'resources': [{u'sendOnSubscribe': False,
        u'vtype': u'number', u'ispublic': True, u'name': u'numero', u'inherit':
        True}], u'name': u'NumberList'}
        """
        datos = self.bclient.getChannel(channel)
        nombre = str(datos['name'])
        return nombre
    
    #Devuelve nombre del recurso indicado
    def getResourceName(self, channel=None, resource=None):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        logging.debug("modo sin conexion : " + str(self.sinConexion))
        if self.sinConexion == False:
            if channel == None:
                channel = self.canal
            if resource == None:
                resource = self.recurso
        #datos es de tipo dict()
        
        datos = self.bclient.getChannel(channel)['resources']
        if len(datos) > 1:
            logging.info("HAY MAS DE UN RECURSO EN EL CANAL DE BEEBOTTE!"
            + " DEVOLVIENDO SOLO EL PRIMERO")
        nombre = str(datos[0]['name'])
        return nombre

    #Devuelve tipo del recurso indicado
    def getResourceType(self, channel=None, resource=None):
        #Creo la instacion de bclient que utilizaré para
        #realizar el resto de operaciones. Al hacerlo
        #también compruebo la conexión con el servidor.
        self.bclient = self.initConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        logging.debug("modo sin conexion : " + str(self.sinConexion))
        if self.sinConexion == False:
            if channel == None:
                channel = self.canal
            if resource == None:
                resource = self.recurso
        
        datos = self.bclient.getChannel(channel)['resources']
        if len(datos) > 1:
            logging.info("HAY MAS DE UN RECURSO EN EL CANAL DE BEEBOTTE!"
            + " DEVOLVIENDO SOLO EL PRIMERO")
        tipo = str(datos[0]['vtype'])
        return tipo

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
            opcion = raw_input("Selecciona operacion:"
            +"\n1.Añadir canal."
            +"\n2.Añadir variable a canal ya existente."
            +"\n3.Borrar canal.\n")
            #Añadir canal
            if opcion == "1":
                nombre = raw_input("Nombre canal: ")
                label = raw_input("Label: ")
                descr = raw_input("Descripcion: ")
                varName = raw_input("Nombre variable: ")
                varType = raw_input("Tipo variable (\"string\" o \"number\": ")
                isPublic = True
                res = self.createChannel(bclient, nombre, varName, varType, label, descr, isPublic, debug)
                logging.debug(res)
            #Añadir variable
            elif opcion == "2":
                canal = raw_input("Canal: ")
                nombre= raw_input("nombre variable: ")
                tipo= raw_input("tipo (string o number): ")
                label= raw_input("label: ")
                descr= raw_input("descripcion: ")
                sendOnSubs = False
                res = self.createResource(bclient, canal, nombre,tipo,label, descr, sendOnSubs, debug)
                logging.debug(res)
            elif opcion == "3":
                nombre = raw_input("Nombre canal: ")
                try:
                    bclient.deleteChannel(nombre)
                except:
                    logging.warning("No se pudo borrar canal "+nombre)
            else:
                logging.debug("opcion no valida")
            
            #continuamos con el bucle
            opcion2 = raw_input("Quiere realizar otra operacion? Y/N: ")
            if(opcion2 != "Y" and opcion2 != "y"):
                repetir = False

    #INTERFAZ PARA CARGAR EN LAS LISTAS GLOBALES
    #LOS DATOS DE LAS BASES DE DATOS.
    #Este metodo se llamará igual tanto en el
    #manejador de SQL como de Beebotte.
    def reload(self):
        self.readRandom()

if __name__ == "__main__":
    #Setup log
    setup_log()
    logging.warning("Iniciado!")
    clase = BeeBasic()
    clase.user_op()
