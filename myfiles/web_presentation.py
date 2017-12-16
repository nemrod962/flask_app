# -*- coding: UTF-8 -*-
"""
Esta librería se encarga de insertar
los resultados obtenidos por web_functions
en código html y pasárselo a Flask para que
este lo muestre a través de render_template
"""

import web_functions
import date_handler

#obtiene la tabla de MySQL y la
#inserta en HTML
def getTableHTML(DBHandler, debug = False):
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

        #obtengo listas 
        listaNum = DBHandler.listaGlobalNumero
        listaDate = DBHandler.listaGlobalFecha
        
   
        l1 = len(listaNum)
        l2 = len(listaDate)
        if l1 != l2:
            print "TableHTML(): LONGITUD DE LISTAS DIFERENTES!"
        if debug:
            print "Longitud de la(s) lista(s): " + str(l1)

   
        #Inicio de la tabla
        tablaHTML = "<style> table, th, td {border: 1px solid black;} </style>"
        #Anchura de la tabla
        tablaHTML += "<table style=\"width:50%\">"
        #PRIMERA FILA
        tablaHTML += "<tr>"
        tablaHTML += "<th>Numero</th><th>FechaMs</th><th>Fecha</th>"        
        tablaHTML += "</tr>"
        #Tantas filas como longitud de la tabla
        for fila in xrange(l1):
            #inicio fila
            tablaHTML += "<tr>"
            #Numero
            tablaHTML += "<th>"+str(listaNum[fila])+"</th>"
            #FechaMs
            tablaHTML += "<th>"+str(listaDate[fila])+"</th>"
            #FechaStr
            tablaHTML += "<th>"+\
            str(date_handler.msToDatetime(listaDate[fila]))\
            +"</th>"
            #fin fila                  
            tablaHTML += "</tr>"
        #fin tabla
        tablaHTML += "</table>"

    return tablaHTML
