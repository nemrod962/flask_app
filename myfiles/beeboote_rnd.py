# -*- coding: utf-8 -*-
"""
INSERTAMOS LOS NUEMRO ALEATORIOS OBTENIDOS
DE LA WEB EN LA BASE DE DATOS DE BEEBOTTE
TAMBIEN APORTA FUNCIONALIDAD PARA TRABAJAR CON
BEEBOTTE
"""
#include beebotte SDK for python
from beebotte import *

#importamos la clase para obtener los numeros aleatorios
import web_fetcher.rnd_fetcher

#Iniciamos la conexion con Beebotte
def initConn():
    #bclient = BBT("API_KEY", "SECRET_KEY")
    _accesskey = "6dcd5477c26e32e1819f487f169f2a45"
    _secretkey = "e6912a135c4da71e9b2d605046f534be154d06f32ac5784f53a562ccb48d336b"
    _hostname = "api.beebotte.com"
    bclient = BBT(_accesskey, _secretkey, hostname = _hostname)
    return bclient

#create channel. Es necesario crear una variable tambien
def createChannel(bclient, channelName, 
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
def createResource(bclient, myChannel, varName, varType="string",
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


#WRITE DATA
def writeData(bclient, channel, varName, value):
    #try:
    #Create a Resource object
    res = Resource(bclient, channel, varName)
    #write to the resource
    res.write(value)
    return 0
    """    
    except:
        print "Could not write value "+value+" into variable "+varName
        return 1
    """

#READ DATA
def readData(bclient, channel, varName, myLimit = 5, debug = False):
    #read resources
    records1 = bclient.read(channel, varName, myLimit)
    if debug:
        print "Estoy leyendo."
        for x in records1:
            print x


#----------------------------------------
"""
Ahora escribimos el numero aleatorio en la base de datos.
Debuelve 0 si se ha realizado satisfactoriamente, 1 si no.
"""
def writeRandom(debug=False):
    #iniciamos conexion con la base ded datos online
    bclient = initConn()
    #obtenemos numero aleatorio de internet
    rndClass = web_fetcher.rnd_fetcher.Rnd_fetcher()
    rndNumber = rndClass.get_web_rnd()
    if debug:
        print "El numero aleatorio es: "+str(rndNumber)
    #escribimos el numero random en la BBDD online
    #es necseraio convertirlo a string para pasarlo como parametro
    success=writeData(bclient, "NumberList", "numero", rndNumber)
    if success == 0:
        if debug:
            print "Numero "+str(rndNumber)+" escrito satisfactoriamente en NumberList"
        return 0
    else:
        if debug:
            print "ERROR: no se pudo escribir el numero "+str(rndNumber)
        return 1
"""
Lee los numeros aleatorios ya esxitentes en la Base de datos online
"""
def readRandom():
    bclient = initConn()
    readData(bclient, "NumberList", "numero", 5, True)

#----------------------------------------

#permite al usuario añadir canales y variables a los mismos
def user_op():
    repetir = True
    bclient = initConn()
    while repetir:
        opcion = raw_input("Selecciona operacion:\n1.Añadir canal.\n2.Añadir variable a canal ya existente.\n3.Borrar canal.\n4.Escribir numero aleatorio.\n5.Ver numeros aleatorios.\n")
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
        if opcion == "2":
            canal = raw_input("Canal: ")
            nombre= raw_input("nombre variable: ")
            tipo= raw_input("tipo (string o number): ")
            label= raw_input("label: ")
            descr= raw_input("descripcion: ")
            res = createResource(bclient, canal, nombre,tipo,label, descr)
            print res
        if opcion == "3":
            nombre = raw_input("Nombre canal: ")
            try:
                bclient.deleteChannel(nombre)
            except:
                print "No se pudo borrar canal "+nombre
        if opcion == "4":
            writeRandom(True)
        if opcion == "5":
            readRandom()
        #opcion no valida
        else:
            print "opcion no valida"
        
        #continuamos con el bucle
        opcion2 = raw_input("Quiere realizar otra operacion? Y/N:\n")
        if(opcion2 != "Y" and opcion2 != "y"):
            repetir = False

if __name__ == "__main__":
    user_op()
