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
        

        while len(DBHandler.listaGlobalNumero) <= 0 :
            print "LISTAS VACIAS. ESPERANDO..."
            time.sleep(1)

        #obtengo listas 
        listaNum = DBHandler.listaGlobalNumero
        listaDate = DBHandler.listaGlobalFecha
        
        l1 = len(listaNum)
        l2 = len(listaDate)
        if l1 != l2:
            print "umbral(): LONGITUD DE LISTAS DIFERENTES!"
        
        if debug:
            print "Longitud de la(s) lista(s): " + str(l1)

        #umbral superior
        resNumSup = umbral
        resDateSup = 0
        #recorro lista entera buscando valor superior
        #al ya exitente en resNumSup
        for index in xrange(l1):
            if listaNum[index] > resNumSup:
                resNumSup = listaNum[index]
                resDateSup = listaDate[index]


        #umbral inferior
        resNumInf = umbral
        resDateInf = 0
        #recorro lista entera buscando valor superior
        #al ya exitente en resNumSup
        for index in xrange(l1):
            if listaNum[index] < resNumInf:
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

        return (resNumSup, resDateSup, resNumInf, resNumInf)

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
        

        while len(DBHandler.listaGlobalNumero) <= 0 :
            print "LISTAS VACIAS. ESPERANDO..."
            time.sleep(1)

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
        
        media = sumatorio/l1
        return media


#3---------------------------------------------------------------
#Mostrar gráficas de beeboote.
