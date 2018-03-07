# -*- coding: UTF-8 -*-

"""
Esta clase se encargara de realizar las funciones
que se utilizarán en la pagina web a la hora de 
ofrecer las funcionalidades al cliente.

Principalmente utilizaremos las listas de los numeros aleatorios
y sus fechas ya sea de las clases SQLHandler o BeeHandler.
"""

import time

#SUPONDREMOS QUE LAS LISTAS DE NUMEROS Y FECHAS NO ESTAN ORDENADAS
#ya que en sql estan en orden descendente de fechas y en beebotte ascendente 


#1---------------------------------------------------------------
#Se especifica un umbral. Se toma el umbral como umbral superior y 
#comprobar si se ha rebasado. Si es asi mostrar la última vez que 
#se hizo mostrando el numero qu elo hizo y su fecha asociada. 
#Repetir el mismo proceso tomando el umbral como uno inferior.
#Se debe especificar la base de datos que se utiliza.
def umbral(DBHandler, umbral, debug = False):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler"\
    or DBHandler.__class__.__name__ == "BeeHandler" :

        #ACTUALIZO LAS LISTAS EN DBHANDLER
        if DBHandler.__class__.__name__ == "BeeHandler":
            DBHandler.readRandom()
            if debug:
                print "Usando Beebotte"
                print DBHandler.listaGlobalFecha
                print DBHandler.listaGlobalNumero

        if DBHandler.__class__.__name__ == "SQLHandler":
            DBHandler.readDataDB()
            if debug:
                print "Usando MySQL"
                print DBHandler.listaGlobalFecha
                print DBHandler.listaGlobalNumero
        
        #No puedo estar esperando a que se llenen. Hay casos
        #en los que no podremos conectarnos a la base de datos de 
        #mysql local, por lo que las listas estarán vacías.
        #Si esperamos a que se llenen, cosa que nunca ocurrirá,
        #colgaremos el programa.
        """
        while len(DBHandler.listaGlobalNumero) <= 0 :
            print "LISTAS VACIAS. ESPERANDO..."
            time.sleep(1)
        """
        #Añado alerta en su lugar
        if len(DBHandler.listaGlobalNumero) <= 0 :
            print "ATENCION: LISTAS VACIAS!"

        #obtengo listas 
        listaNum = DBHandler.listaGlobalNumero
        listaDate = DBHandler.listaGlobalFecha
        
        l1 = len(listaNum)
        l2 = len(listaDate)
        if l1 != l2:
            print "umbral(): LONGITUD DE LISTAS (fecha y número) DIFERENTES!"
        elif debug:
            print "Longitud de la(s) lista(s): " + str(l1)

        #umbral superior
        resNumSup = umbral
        resDateSup = 0
        #recorro lista entera buscando valor superior
        #al especificado por el umbral.
        #Si l1 == 0, no se llega a entrar en el for,
        #por lo que seria a prueba de errores.
        for index in xrange(l1):
            if listaNum[index] > umbral:
                #Nos quedaremos con el ULTIMO 
                #numero que haya superado e umbral
                if listaDate[index] > resDateSup:
                    resNumSup = listaNum[index]
                    resDateSup = listaDate[index]


        #umbral inferior
        resNumInf = umbral
        resDateInf = 0
        #recorro lista entera buscando valor inferior
        #al especificado por el umbral.
        #Si l1 == 0, no se llega a entrar en el for,
        #por lo que seria a prueba de errores.
        for index in xrange(l1):
            if listaNum[index] < umbral:
                #Nos quedaremos con el ULTIMO 
                #numero que haya superado el umbral
                #por debajo
                if listaDate[index] > resDateInf:
                    resNumInf = listaNum[index]
                    resDateInf = listaDate[index]
        
        if debug:
            print "Resultado:"
            if resNumSup == umbral:
                print "No se ha superado el umbral como umbral superior"
            else:
                print "Superior: " + str(resNumSup) + " - " + str(resDateSup)
            if resNumInf == umbral:
                print "No se ha superado el umbral como umbral inferior"
            else:
                print "Inferior: " + str(resNumInf) + " - " + str(resDateInf)

        return (resNumSup, resDateSup, resNumInf, resDateInf)

    #Base de datos desconocida
    else:
        print "Base de datos desconocida"




#2---------------------------------------------------------------
#Calcular el valor medio de los numeros almacenados. Se debe especificar
#la base de datos que se ha empleado.
def media(DBHandler, debug = True):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler"\
    or DBHandler.__class__.__name__ == "BeeHandler" :

        #ACTUALIZO LAS LISTAS EN DBHANDLER
        if DBHandler.__class__.__name__ == "BeeHandler":
            DBHandler.readRandom()
            if debug:
                print "Usando Beebotte"
                print DBHandler.listaGlobalFecha
                print DBHandler.listaGlobalNumero

        if DBHandler.__class__.__name__ == "SQLHandler":
            DBHandler.readDataDB()
            if debug:
                print "Usando MySQL"
                print DBHandler.listaGlobalFecha
                print DBHandler.listaGlobalNumero
        

        #No puedo estar esperando a que se llenen. Hay casos
        #en los que no podremos conectarnos a la base de datos de 
        #mysql local, por lo que las listas estarán vacías.
        #Si esperamos a que se llenen, cosa que nunca ocurrirá,
        #colgaremos el programa.
        """
        while len(DBHandler.listaGlobalNumero) <= 0 :
            print "LISTAS VACIAS. ESPERANDO..."
            time.sleep(1)
        """
        #Añado alerta en su lugar
        if len(DBHandler.listaGlobalNumero) <= 0 :
            print "ATENCION: LISTAS VACIAS!"

        #obtengo listas 
        listaNum = DBHandler.listaGlobalNumero
        listaDate = DBHandler.listaGlobalFecha
        
        l1 = len(listaNum)
        l2 = len(listaDate)
        if l1 != l2:
            print "umbral(): LONGITUD DE LISTAS DIFERENTES!"
        
        if debug:
            print "Longitud de la(s) lista(s): " + str(l1)

        #calculo de la media
        sumatorio = 0.0

        for index in xrange(l1):
            sumatorio += listaNum[index]
        
        #Si l1 == 0, no hay numeros en las listas,
        #por lo que no se ha podido leer de las bases de datos.
        if l1==0:
            media = "-"
        else:
            media = sumatorio/l1
        return media


#Anexo---------------------------------------------------------------
#Dado como argumento un manejador de BD nos dice si 
#es de MySQL o Beebotte. Se empleará para obtener el 
#tipo de base de datos que se esta utilizando dado
#su manejador
def getDBName(DBHandler):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler":
        return "MySQL (local)"
    elif DBHandler.__class__.__name__ == "BeeHandler" :
        return "Beebotte (online)"
    else:
        return "Descon."

def getDBSimpleName(DBHandler):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler":
        return "mysql"
    elif DBHandler.__class__.__name__ == "BeeHandler" :
        return "beebotte"
    else:
        return "desconocido"
