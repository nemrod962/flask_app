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
#--------------------------------------------------
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
#--------------------------------------------------
   
        l1 = len(listaNum)
        l2 = len(listaDate)
        if l1 != l2:
            print "TableHTML(): LONGITUD DE LISTAS DIFERENTES!"
        if debug:
            print "Longitud de la(s) lista(s): " + str(l1)

        #CREACION DE LA TABLA HTML  
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



def getUmbralHTML(DBHandler, umbral, debug=False):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler"\
    or DBHandler.__class__.__name__ == "BeeHandler" :
        #Obtenemos el resultado con el siguiente formato:
        #tuple(numSup, fechaNumSup, numInf, fechaNumInf)
        tuplaResUmbral = web_functions.umbral(DBHandler, umbral, debug)
        
        #HTML
        #Inicio de la tabla
        tablaHTML = "<style> table, th, td {border: 1px solid black;} </style>"
        #Anchura de la tabla
        tablaHTML += "<table style=\"width:50%\">"
        #PRIMERA FILA
        tablaHTML += "<tr>"
        tablaHTML += "<th>Ultimo Numero Superior</th>"+\
        "<th>Fecha Ultimo Numero Superior</th>" +\
        "<th>Ultimo Numero Inferior</th>"+\
        "<th>Fecha Ultimo Numero Inferior</th>"
        tablaHTML += "</tr>"
        #DATOS
        tablaHTML += "<tr>"
        tablaHTML += "<th>"+ str(tuplaResUmbral[0]) +"</th>"+\
        "<th>"+str(date_handler.msToDatetime(tuplaResUmbral[1])) +"</th>" +\
        "<th>"+str(tuplaResUmbral[2]) +"</th>"+\
        "<th>"+str(date_handler.msToDatetime(tuplaResUmbral[3])) +"</th>"
        tablaHTML += "</tr>"
        #Fin Tabla
        tablaHTML += "</table>"
        
        return tablaHTML



def getMediaHTML(DBHandler, debug=False):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler"\
    or DBHandler.__class__.__name__ == "BeeHandler" :
        #Obtenemos la media de los datos
        media = web_functions.media(DBHandler, debug)

        #Insertamos los datos en HTML
        #Inicio de la tabla
        tablaHTML = "<style> table, th, td {border: 1px solid black;} </style>"
        #Anchura de la tabla
        tablaHTML += "<table style=\"width:50%\">"
        #PRIMERA FILA
        tablaHTML += "<tr>"
        tablaHTML += "<th>Media</th>"
        tablaHTML += "</tr>"
        #DATOS
        tablaHTML += "<tr>"
        tablaHTML += "<th>"+str(media)+"</th>"
        tablaHTML += "</tr>"
        #Fin Tabla
        tablaHTML += "</table>"
        
        return tablaHTML

