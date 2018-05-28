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
    def __init__(self):
        """
        Modoa prueba de fallos. En caso de que no se pueda conectar
        con Beebotte, se activará este modo, de forma
        que esta clase no realizará ninguna función pero evitara el 
        crasheo de la aplicación.
        En un principio stará desactivado, pero si fallamos al conectar
        a la base da datos en la funcion initConn(), lo activamos.
        """
        self.sinConexion=False

    

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
            bclient.read("NumberList", "numero", 1)
        except:
            logging.warning("No se pudo conectar con Beebotte.")
            self.sinConexion=True
            logging.debug("Beebotte - Modo sin conexion: " +
            str(self.sinConexion))

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
                    debug=False
                    ):
        #Si no podemos conectar con la Beebotte, no hacemos nada.
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
                logging.warning("Error when creating channel "+channelName)
                return 1

        
    #ADD RESOURCE. Añade una 'variable' al canal.
    #El canal debe existir.
    #los tipos de la variable pueden ser "string" o "number".
    def createResource(self, bclient, myChannel, varName, varType="string",
                        myLabel = "label", descr = "description",
                        isSendOnSubscribe=False, debug=False):
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
            logging.warning("Could not write value "+ str(value) +
                " into variable " + str(varName))
            return 1
        

    #READ DATA
    def readData(self, bclient, channel, varName, myLimit = 5, debug = False):
        #read resources
        records = bclient.read(channel, varName, myLimit)
        if debug:
            logging.debug("Estoy leyendo.")
            for x in records:
                logging.debug(x)
        return records

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
