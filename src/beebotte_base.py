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
    def __init__(self,canal="NumberList",recurso="numero",tipoRecurso="number"):
        
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
        self.canal = str(canal)
        #Recurso dentro del canal.
        #De él leeremos y escribiremos los datos.
        self.recurso = str(recurso)
        #Este atributo lo utlizaré únicamente si
        #necesito crear el recurso, para saber que 
        #tipo ponerle.
        self.tipoRecurso = str(tipoRecurso)
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
        #realizar el resto de operaciones.
        self.bclient = self.initConn()
        #Compruebo conexion al servidor
        self.checkConn()

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
            logging.warning("No se pudo abrir archivo credenciales: " + str(e))
            self.sinConexion=True
            logging.debug("Beebotte - Modo sin conexion: " +
            str(self.sinConexion))

        _hostname = "api.beebotte.com"
        bclient = BBT(_accesskey, _secretkey, hostname = _hostname)
        return bclient

    #Comprobamos la conexion con Beebotte
    def checkConn(self):
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
            self.bclient.read(self.canal, self.recurso, 1)
        
        except requests.exceptions.ConnectionError as e:
            logging.warning("No hay conexion con Beebotte: "
            + str(e))
            self.sinConexion=True

        except NotFoundError as e:
            #procedo a crearlos. Si devuleve true,
            #es que se han creado stasifactoriamente
            res = self.checkChannelAndResource()
            self.sinConexion= not res
            logging.warning("El canal o recurso de la clase no existen: " 
            + str(e))
            logging.warning("Exito al crearlos: " + str(res))



#-------------------------------------------------------------------------
    """
    Funciones para escribir y leer datos de la base de datos online
    """
    #WRITE DATA
    def writeData(self, channel, varName, value, debug = False):
        #Compruebo conexion con Beebotte
        self.checkConn()
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
        #Compruebo conexion con Beebotte
        self.checkConn()
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if debug:
            logging.debug("modo sin conexion : " +
            str(self.sinConexion))
        if self.sinConexion == False:
            #read resources
            records = self.bclient.read(channel, varName, myLimit)
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

    #Comprueba la existencia del canal y del recurso de la clase.
    #Si no existe alguno de los dos, lo crea.
    def checkChannelAndResource(self,canal=None,recurso=None):
        if canal == None:
            canal = self.canal
        if recurso == None:
            recurso = self.recurso
        #Compruebo canal
        existeCanal = self.getChannelName(canal) != 0
        logging.debug("Ya existe canal: "+canal+" ? "+str(existeCanal))
        res1=True
        #Si no existen los creo
        if not existeCanal:
            res = self.createChannel(self.canal,self.recurso,self.tipoRecurso)
            if res == 0:
                logging.debug("Exito al crear canal: " + self.canal)
                res1 = True
            else:
                logging.warning("No se pudo crear canal: " + self.canal)
                res1 = False
        #compruebo recurso
        existeRecurso = self.getResourceName(recurso, canal) != 0
        logging.debug("Ya existe rec: "+recurso+" ? "+str(existeRecurso))
        res2=True
        if not existeRecurso:
            res = self.createResource(self.canal,self.recurso,self.tipoRecurso)
            if res == 0:
                logging.debug("Exito al crear recurso: " + self.recurso)
                res2 = True
            else:
                logging.warning("No se pudo crear recurso: " + self.recurso)
                res2 = False
        return res1 and res2
    

    #create channel. Es necesario crear una variable tambien.
    def createChannel(self, channelName, 
                    #parametros de la varable
                    varName, varType="number",
                    #parametros canal
                    myLabel="channel label", 
                    descr="channel description", isPublic=True,
                    debug=False
                    ):
        #Formato variables
        channelName = str(channelName)
        varName = str(varName)

        #logging.debug("createChannel - modo sin conexion : "+str(self.sinConexion))

        #Creo el canal en caso de que no exista ya 
        #y de que haya conexion
        yaexiste = self.getChannelName(channelName) != 0
        logging.info("yaexiste " + channelName + " ? " + str(yaexiste))
        if not yaexiste:
            logging.info("Creating channel: " + str(channelName) + " with var: "
            + varName)
            try:
                if varType == "string":
                    self.bclient.addChannel(
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
                    self.bclient.addChannel(
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
            except Exception as e:
                logging.warning("Error when creating channel "+channelName
                + ". ERROR: " + str(e))
                return 1

        
    #ADD RESOURCE. Añade una 'variable' al canal.
    #El canal debe existir.
    #los tipos de la variable pueden ser "string" o "number".
    def createResource(self, myChannel, varName, varType="number",
                        myLabel = "label", descr = "description",
                        isSendOnSubscribe=False, debug=False):
        #Formato variables
        channelName = str(myChannel)
        varName = str(varName)
        varType=str(varType)

        #Creo el recurso en caso de que no exista ya 
        #y de que haya conexion
        yaexiste = self.getResourceName(varName, channelName) != 0
        logging.info("ya existe recurso: " + varName 
        + " en " + channelName+" ? " + str(yaexiste))

        #Si no podemos conectar con la Beebotte, no hacemos nada.
        #logging.debug("createResource - modo sin conexion : " + str(self.sinConexion))
        if not yaexiste:
            if varType == "string":
                try:
                    self.bclient.addResource(
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
                    self.bclient.addResource(
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
        logging.debug("Borrando canal: " + str(channel))
        return self.bclient.deleteChannel(str(channel))
        

    #REMOVE RESOURCE
    def deleteResource(self, channel, resource):
        #parse arguments
        channel = str(channel)
        resource = str(resource)
        logging.debug("Borrando recurso: " + str(resource)
        + " del canal: " + str(channel))
        res = self.bclient.deleteResource(channel, resource)
        return res

    #RESET CHANNEL
    def resetChannel(self, channel=None, varName=None, varType=None ,\
    myLabel="channel label", descr="channel description",\
    isPublic=True,debug=False):
        #Si no se especifican parametros, utilizo los de la instancia
        if channel == None:
            channel = self.canal
        if varName == None:
            varName = self.recurso
        if varType == None:
            varType = self.tipoRecurso
        logging.info("Nombre Res: " + str(varName))
        logging.info("Tipo Res: " + str(varType))
        #Borro canal
        self.deleteChannel(channel)
        #lo vuelvo a crear
        self.createChannel(channel,varName,varType,myLabel,\
        descr, isPublic, debug)

    #RESET RESOURCE
    def resetResource(self, channel=None, varName=None, varType=None,\
    myLabel="channel label", descr="channel description",\
    sendOnSubs=False, debug=False):
        #Si no se especifican parametros, utilizo los de la instancia
        if channel == None:
            channel = self.canal
        if varName == None:
            varName = self.recurso
        if varType == None:
            varType = self.tipoRecurso
        logging.info("Nombre Res: " + str(varName))
        logging.info("Tipo Res: " + str(varType))
        #Borro canal
        self.deleteResource(channel, varName)
        #lo vuelvo a crear
        self.createResource(channel,varName,varType,myLabel,\
        descr, sendOnSubs, debug)

    #Devuelve nombre del canal indicado.
    #Devuelve nombre del canal de la instancia si
    #no se indica ninguno.
    #Devuelve 0 si no existe o no se encuentra.
    def getChannelName(self, channel=None):
        #Si no podemos conectar con la Beebotte, no hacemos nada.
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
        try:
            datos = self.bclient.getChannel(channel)
            #Si datos contiene los datos de mas de un canal
            #sera de tipo list. Si solo contiene datos de un 
            #canal sera de tipo dict
            if len(datos) > 1 and type(datos) == list:
                logging.info("HAY MAS DE UN CANAL EN BEEBOTTE!"
                + " DEVOLVIENDO SOLO EL PRIMERO")
                nombre = str(datos[0]['name'])
            #Solo un canal. Tipo dict
            else:
                nombre = str(datos['name'])
        except NotFoundError as e:
            logging.warning("ERROR: " + str(e))
            nombre = 0
        return nombre
    
    #Devuelve nombre del primer recurso del canal indicado.
    #No muy útil si el canal tiene mas de un recurso.
    #Devuelve 0 si no existe o no se encuentra.
    def getResourceName(self, resource=None, channel=None):
        #Si no podemos conectar con la Beebotte, no hacemos nada.
        if channel == None:
            channel = self.canal
        if resource == None:
            resource = self.recurso
        #default value. Lo devolvemos si njo se encuentra nada.
        nombre = 0
        #datos es de tipo dict()
        try:
            datos = self.bclient.getChannel(channel)['resources']
            if len(datos) > 0:
                for i in datos:
                    if str(i['name']) == resource:
                        nombre = str(i['name'])
        except NotFoundError as e:
            logging.warning("ERROR: " + str(e))
        return nombre

    #Devuelve tipo del primer recurso del canal indicado.
    #No muy útil si el canal tiene mas de un recurso.
    #Devuelve 0 si no existe o no se encuentra.
    def getResourceType(self, resource=None, channel=None):
        if channel == None:
            channel = self.canal
        if resource == None:
            resource = self.recurso
        #default value. Lo devolvemos si njo se encuentra nada.
        tipo = 0
        try:
            datos = self.bclient.getChannel(channel)['resources']
            if len(datos) > 0:
                for i in datos:
                    if str(i['name']) == resource:
                        tipo = str(i['vtype'])
        except NotFoundError as e:
            logging.warning("ERROR: " + str(e))
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
            +"\n0.Ver canales."
            +"\n1.Añadir canal."
            +"\n2.Añadir variable a canal ya existente."
            +"\n3.Borrar canal."
            +"\n4.Borrar recurso."
            +"\n5.Reiniciar canal."
            +"\n6.Reiniciar recurso."
            +"\n")
            #Ver canales
            if opcion == "0":
                print(self.bclient.getChannel())
            #Añadir canal
            elif opcion == "1":
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
            #BorrarCanal
            elif opcion == "3":
                nombre = raw_input("Nombre canal: ")
                try:
                    self.deleteChannel(nombre)
                except Exception as e:
                    logging.warning("No se pudo borrar canal "+nombre
                    +". Error: " + str(e))
            #BorrarRecurso
            elif opcion == "4":
                nombreC = raw_input("Nombre canal: ")
                nombreR = raw_input("Nombre recurso: ")
                try:
                    self.deleteResource(nombreC, nombreR)
                except Exception as e:
                    logging.warning("No se pudo borrar recurso "+nombreR
                    +". Error: " + str(e))
            #ReiniciarCanal
            elif opcion == "5":
                nombreC = raw_input("Nombre canal: ")
                if nombreC == "":
                    nombreC = None
                nombreR = raw_input("Nombre recurso: ")
                if nombreR == "":
                    nombreR = None
                try:
                    self.resetChannel(nombreC, nombreR)
                except Exception as e:
                    logging.warning("No se pudo reiniciar canal "+nombreR
                    +". Error: " + str(e))
            #ReiniciarRecurso
            elif opcion == "6":
                nombreC = raw_input("Nombre canal: ")
                if nombreC == "":
                    nombreC = None
                nombreR = raw_input("Nombre recurso: ")
                if nombreR == "":
                    nombreR = None
                try:
                    self.resetResource(nombreC, nombreR)
                except Exception as e:
                    logging.warning("No se pudo reiniciar recurso "+nombreR
                    +". Error: " + str(e))
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
    logging.info("Iniciado!")
    clase = BeeBasic("test", "test")
    clase.user_op()
