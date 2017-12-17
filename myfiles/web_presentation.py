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


#Dado un umbral, obtiene los resultados tras consultar
#la base de datos especificada y devuelve una tabla
#HTML con los mismos.
def getUmbralHTML(DBHandler, umbral, debug=False):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler"\
    or DBHandler.__class__.__name__ == "BeeHandler" :
        #Obtenemos el resultado con el siguiente formato:
        #tuple(numSup, fechaNumSup, numInf, fechaNumInf)
        tuplaResUmbral = web_functions.umbral(DBHandler, umbral, debug)
        
        #Paso el formato de fecha de ms a datetime
        tuplaResUmbral=(tuplaResUmbral[0],\
        str(date_handler.msToDatetime(tuplaResUmbral[1])),\
        tuplaResUmbral[2],\
        str(date_handler.msToDatetime(tuplaResUmbral[3]))) 

        #COMPROBACION DE RESULTADOS
        """
        Si el resultado superior es igual al umbral,
        significa que no se ha hallado resultado considerando 
        el umbral como un umbral superior (No hay numero que supere
        al umbral). Lo mismo pasa con el resultado inferior.
        """
        #Superior
        #Si no hay un numero superior al umbral,
        #no muestro ni numero ni fecha
        if tuplaResUmbral[0] == umbral:
            tuplaResUmbral=(" - ", " - " ,tuplaResUmbral[2],tuplaResUmbral[3]) 
        #Inferior
        #Si no hay un numero inferior al umbral,
        #no muestro ni numero ni fecha
        if tuplaResUmbral[2] == umbral:
            tuplaResUmbral=(tuplaResUmbral[0],tuplaResUmbral[1]," - ", " - ") 

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
        "<th>"+str(tuplaResUmbral[1]) +"</th>" +\
        "<th>"+str(tuplaResUmbral[2]) +"</th>"+\
        "<th>"+str(tuplaResUmbral[3]) +"</th>"
        tablaHTML += "</tr>"
        #Fin Tabla
        tablaHTML += "</table>"
        
        return tablaHTML

        #"<th>"+str(date_handler.msToDatetime(tuplaResUmbral[1])) +"</th>"
        #"<th>"+str(date_handler.msToDatetime(tuplaResUmbral[3])) +"</th>"

#Obtiene la media de los datos alamcenados en un
#base de datos y devuelve el resultado en forma
#de tabla HTML
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

