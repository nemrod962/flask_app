# -*- coding: UTF-8 -*-
#FLASK
from flask import Flask, render_template, url_for,\
redirect, request, make_response, Blueprint, current_app
#Manejo Bases de Datos
from sql_rnd import SQLHandler
from beebotte_rnd import BeeHandler
from mongo_rnd import MongoHandler
#Usuarios en Bases de Datos
from mongo_user import UserManager
from mongo_oauth import OAuthUserManager
#Dada la clase me devuelve el nombre
from db_name_getter import getDBName, getDBSimpleName
#Log
import logging
from log_handler import setup_log
#Views
from blue_cookie import getCookieUserName, getCookieDB

blueApp = Blueprint('blueApp', __name__)

"""
  __  __                    ____       _            _             _ 
 |  \/  | ___ _ __  _   _  |  _ \ _ __(_)_ __   ___(_)_ __   __ _| |
 | |\/| |/ _ \ '_ \| | | | | |_) | '__| | '_ \ / __| | '_ \ / _` | |
 | |  | |  __/ | | | |_| | |  __/| |  | | | | | (__| | |_) | (_| | |
 |_|  |_|\___|_| |_|\__,_| |_|   |_|  |_|_| |_|\___|_| .__/ \__,_|_|
                                                     |_|            
"""
#PAGINA INICIAL
#menú principal
#Mostramos la pagina inicial
@blueApp.route("/", methods=['GET','POST'])
def webMain():
    if request.method == 'GET':
        nombreUsuario = getCookieUserName(request)
        #Obtengo el manejador de la BD a 
        #utilizar según la cookie del usuario.
        DBHandler = getCookieDB(request)
        logging.debug("MAIN: Usuario - " + str(nombreUsuario))
        #---
        response = make_response(render_template("index.html",\
        DBName = getDBName(DBHandler),\
        username=nombreUsuario))

        #if sehaborrado:
        #    response.set_cookie('expired','1')
        return response
    elif request.method == 'POST':
        logging.debug("MAIN POST")
        opcion = request.form.get('opcion', "elegir")
        #opcion = request.form['option']
        #opcion=request.args.get('option','default',type=str)

        umbraltxt = request.form.get('umbralTxt',"error")
        #umbraltxt = request.form['umbralTxt']
        #umbraltxt=request.args.get('umbralTxt','50',type=str)
        logging.debug("OPCION: " + opcion    )
        logging.debug("umbraltxt: " + umbraltxt)
        #Dependiendo de la direccion seleccionada en
        #la pantalla inicial redirigiremos a una dirección 
        #o a otra.
        if opcion == "elegir":
            return url_for('blueApp.pruebajs0')
        if opcion == "tablas":
            #return redirect(url_for('show_type', sensor="s1"))
            return url_for('blueApp.pruebajs1')
        if opcion == "umbral":
            #Evitar cadena vacia
            if umbraltxt == "":
                umbraltxt = "error"
            return url_for('blueApp.pruebajs2', umb = umbraltxt)
        if opcion == "media":
            return url_for('blueApp.pruebajs3')
        if opcion == "grafoBee":
            return url_for('blueApp.pruebajs4')
        if opcion == "grafo":
            return url_for('blueApp.pruebajs5')
        else:
            return "ERROR: Opción Desconocida"
    

"""
    JavaScript
"""

#ELEGIR DB
@blueApp.route("/prueba0", methods=['GET','POST'])
def pruebajs0():
    if request.method == 'GET':
        return render_template("DBselect.html")
    elif request.method == 'POST':
        #opcion = request.form.get('chosenDB',"default")
        opcion = request.form.get('opcion',"default")
        #Para permitir realmente la concurrencia de usuarios, 
        #haremos que la base de datos a emplear se almacene 
        #en las cookies del usuario, de forma que
        #cada uno tenga su valor.
        #
        #Creo la respuesta a la que asignaré las cookies
        response = make_response(redirect(url_for('blueApp.webMain')))
        #Asigno la base de datos seleccionada al cliente
        if opcion == "MySQL":
            #DBHandler = SQLHandler
            pass
        elif opcion == "Beebotte":
            #DBHandler = BeeHandler
            pass
        elif opcion == "MongoDB":
            #DBHandler = MongoHandler
            pass
        else:
            logging.info("DB seleccionada descon.")
            #base de datos mongoDB por defecto
            opcion="MongoDB"
        #Guardo la base de datos seleccionada en la cookie
        #del cliente.
        #Utilizare la funcion getCookieDB() para, dada
        #la peticion, obtener la cookie del cliente y
        #de alli la base de datos a emplear
        response.set_cookie('db',opcion)
        return response

#TABLAS_JS
@blueApp.route('/prueba')
def pruebajs1():
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    DBName = getDBSimpleName(DBHandler)
    logging.debug("lista en pruebajs: " + str(listaNum))
    return render_template("tablas.html", listaNum=listaNum,
    listaDate=listaDate, DBName=DBName)

#UMBRAL_JS
@blueApp.route("/prueba2/<umb>")
def pruebajs2(umb):
    #Obtengo el manejador de la BD a 
    #utilizar según la cookie del usuario.
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    DBName = getDBSimpleName(DBHandler)
    #Obtengo el umbral
    try:
        trueUmbral = float(umb)
    except ValueError:
        logging.info("NO SE HA INTRODUCIDO NUMERO COMO UMBRAL!")
        #umb = "Debe introducirse un numero. Usando valor por defecto: 50."
        trueUmbral = 50
    logging.debug("Umbral a emplear")
    logging.debug("str: " + umb)
    logging.debug("float: " + str(trueUmbral))
    return render_template("umbral.html",\
    listaNum=listaNum,
    listaDate=listaDate, 
    DBName=DBName,
    umbral= umb)
    #resUmbral = "<div>HOLA</div>")

#Media
@blueApp.route('/prueba3')
def pruebajs3():
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    DBName = getDBSimpleName(DBHandler)
    logging.debug("lista en pruebajs: " + str(listaNum))
    return render_template("media.html", listaNum=listaNum,
    listaDate=listaDate, DBName=DBName)

#Graficas Beebotte
@blueApp.route('/prueba4')
def pruebajs4():
    return render_template("grafoBee.html")

#Graficas Plotly
@blueApp.route('/prueba5')
def pruebajs5():
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    DBName = getDBSimpleName(DBHandler)
    
    return render_template("grafoJs.html", listaNum=listaNum,
    listaDate=listaDate, DBName=DBName);
