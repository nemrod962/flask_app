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
#Generar num aleatorios
import random
#Log
import logging
from log_handler import setup_log
#Views
from blue_cookie import getCookieUserName, getCookieDB, no_cookie_check

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
            return url_for('blueApp.webSelectDB')
        if opcion == "tablas":
            #return redirect(url_for('show_type', sensor="s1"))
            return url_for('blueApp.webTabla')
        if opcion == "umbral":
            #Evitar cadena vacia
            if umbraltxt == "":
                umbraltxt = "error"
            return url_for('blueApp.webUmbral', umb = umbraltxt)
        if opcion == "media":
            return url_for('blueApp.webMedia')
        if opcion == "grafoBee":
            return url_for('blueApp.webGrafoBee')
        if opcion == "grafo":
            return url_for('blueApp.webGrafo')
        else:
            return "ERROR: Opción Desconocida"
    

"""
    JavaScript
"""

#ELEGIR DB
@blueApp.route("/selectDB", methods=['GET','POST'])
#def pruebajs0():
def webSelectDB():
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
        response = make_response(url_for('blueApp.webMain'))
        #Asigno la base de datos seleccionada al cliente
        if opcion.lower() == "MySQL".lower():
            opcion = "MySQL"
            #DBHandler = SQLHandler
            pass
        elif opcion.lower() == "Beebotte".lower():
            opcion = "Beebotte"
            #DBHandler = BeeHandler
            pass
        elif opcion.lower() == "MongoDB".lower():
            opcion = "MongoDB"
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
@blueApp.route('/tabla')
#def pruebajs1():
def webTabla():
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    DBName = getDBSimpleName(DBHandler)
    logging.debug("lista en pruebajs: " + str(listaNum))
    return render_template("tablas.html", listaNum=listaNum,
    listaDate=listaDate, DBName=DBName)

#UMBRAL_JS
@blueApp.route("/umbral")
#def pruebajs2(umb):
def webUmbral():
    #Obtengo el manejador de la BD a 
    #utilizar según la cookie del usuario.
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    DBName = getDBSimpleName(DBHandler)
    return render_template("umbral.html",\
    listaNum=listaNum,
    listaDate=listaDate, 
    DBName=DBName)
    #resUmbral = "<div>HOLA</div>")

#Media
@blueApp.route('/media')
#def pruebajs3():
def webMedia():
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    DBName = getDBSimpleName(DBHandler)
    return render_template("media.html", listaNum=listaNum,
    listaDate=listaDate, DBName=DBName)

#Graficas Beebotte
@blueApp.route('/grafoBee')
#def pruebajs4():
def webGrafoBee():
    return render_template("grafoBee.html")

#Graficas Plotly
@blueApp.route('/grafo')
#def pruebajs5():
def webGrafo():
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    DBName = getDBSimpleName(DBHandler)
    
    return render_template("grafoJs.html", listaNum=listaNum,
    listaDate=listaDate, DBName=DBName);

#Devuelve un numero aleatorio aleatorio de la base de datos
@blueApp.route('/random')
def webRandom():
    DBHandler = getCookieDB(request)
    listaNum = DBHandler.listaGlobalNumero
    listaDate = DBHandler.listaGlobalFecha
    
    DBName = getDBSimpleName(DBHandler)
    return render_template("random.html", listaNum=listaNum,
    listaDate=listaDate, DBName=DBName)

#Muestra la página 'About'
@blueApp.route('/about')
def webAbout():
    return render_template("about.html")

#Muestra la gráfica de Beebotte
@blueApp.route('/bee')
@no_cookie_check
def webBeeGrafica():
    return render_template("beebotte.html")
