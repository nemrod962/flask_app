# -*- coding: UTF-8 -*-
"""
EJEMPLO INICIAL DE FLASK
"""
#FLASK
from flask import Flask, render_template, url_for,\
redirect, request, make_response, Blueprint, current_app
#Manejo Bases de Datos
import sql_rnd
import beebotte_rnd
import mongo_rnd
#Usuarios en Bases de Datos
from mongo_user import UserManager
from mongo_oauth import OAuthUserManager
#Log
import logging
from log_handler import setup_log, setStreamMode

"""
   ____            _    _         ____ _               _    
  / ___|___   ___ | | _(_) ___   / ___| |__   ___  ___| | __
 | |   / _ \ / _ \| |/ / |/ _ \ | |   | '_ \ / _ \/ __| |/ /
 | |__| (_) | (_) |   <| |  __/ | |___| | | |  __/ (__|   < 
  \____\___/ \___/|_|\_\_|\___|  \____|_| |_|\___|\___|_|\_\
                                                            
"""

blueCookie = Blueprint('blueCookie', __name__)

#Añade el atributo '_exclude_from_checking' a la funcion recibida
#como parámetra. Este atributo añadido a la función indicará al
#request_hook que no se comprueben las cookies para la dirección
#asociada a la view function que posee este atributo.
#Esta función para añadir un atributo a otra función se
#utilizará en forma de label.
#Si, por ejemplo, se quiere excluir a la funcion webLogin() 
#de la comprobación de cookies habrá que añadir la siguiente 
#línea nates de la declaración de la función
# @no_cookie_check
#de forma que quedará así:
# @app.route('/login')
# @no_cookie_check
# def webLogin():
# ...
def no_cookie_check(func):
    func._exclude_from_checking = True
    return func


#Se establecerá un request hook para comprobar las cookies de sesion, de forma
#que nos aseguraremos de que el cliente haya iniciado sesión y esta no ha
#caducado al acceder a ciertas partes de la aplicación (la gran mayoría.
#Excepciones: login y registro).
#Un request hook es una función que se ejecutará cada vez que se reciba una
#petición del cliente (request)
#
#En blueprint:
#
#Blueprint.before_app_request(f)
#Like Flask.before_request(). Such a function is executed before 
#each request, even if outside of a blueprint.

@blueCookie.before_app_request
def check_cookies(*args, **kwargs):
    #BLueprints
    #Importo dentro de esta funcion
    #para no crear un bucle de imports
    #Necesito blueUser para la redireccionar
    #a la página de /login -> webLogin
    #url_for('blueUser.webMain')
    #from blue_user import blueUser
    #from blue_app import blueApp

    #Creo instancia del manjador de usuarios local
    UserHandler = UserManager()
    #Creo instancia del manejador de usuarios OAuth
    OAuthHandler = OAuthUserManager()
    #Obtengo la instancia base de Flask para
    #poder acceder a todas las view functions
    app = current_app._get_current_object()
    #default value.
    #Indica si hay que ejecutar el checkeo o no
    run_check=True

    #request.endpoint es la peticion al servidor
    #app.view_functions contiene todas las view functions 
    #definidas en la app.
    #
    #Si se cumple este if, significa que la ruta pedida por el cliente
    #es correcta y hay una view funciton asociada a ella
    if request.endpoint in app.view_functions:
        #Obtengo en view_func la funcion que se tiene que ejecutar
        #al acceder a la ruta que ha pedido el cliente.
        #Si por ejemlo se ha pedido la ruta '/', en view_func
        #tendremos al funcion webMain().
        view_func = app.view_functions[request.endpoint]
        #Si la view function en custión no tiene un atributo
        #llamado '_exclude_from_checking', realizaremos una 
        #comprobación de las cookies de sesión antes de ejecutar la
        #view function.
        #run_check= not hasattr(view_func, '_exclude_from_checking')
        #También hay que asegurarse de que la cadena '/static/' no 
        #esté contenida en la URL de la petición, ya que si no, no 
        #se podrán servir sus contenidos (código javascript y css)
        #a no ser que se haya iniciado sesión previamente, por lo que
        #pantallas como la de login no mostrarán el estilo.
        run_check= not hasattr(view_func, '_exclude_from_checking') \
        and '/static/' not in request.path
        #DEBUG. Muestro datos
        if '/static/' not in request.path:
            logging.info('-~> Checkear cookies en %s? %s',str(request.path),
        str(run_check))
        if run_check:
            #En la comprobación verifico que la sesión que indican
            #las cookies del usuario no está caducada. Si no existen se
            #da por hecho que no ha iniciado sesión. En ambos casos, habrá
            #que iniciarla.
            #
            #Obtengo tipo de Cookie : local o OAuth
            idTipo=request.cookies.get('tipoLogin')
            #Obtengo valor Cookie
            idSesion=request.cookies.get('SessionId')
            #Inicializo nombreUsuario
            nombreUsuario=None

            if idTipo=="local":
                #CADUCIDAD - BORRO Y ACTUALIZO
                sehaborrado=UserHandler.checkCookieStatus(idSesion)
                #Si la cookie ha caducado, me mostrara None como Usuario
                nombreUsuario = UserHandler.getCookieUserName(idSesion)
            elif idTipo=="oauth":
                #CADUCIDAD - BORRO Y ACTUALIZO
                sehaborrado=OAuthHandler.checkCookieStatus(idSesion)
                #Si la cookie ha caducado, me mostrara None como Usuario
                idUsuario = OAuthHandler.getCookieUserName(idSesion)
                nombreUsuario = OAuthHandler.getUserName(idUsuario)

            #DEBUG. Muesto info
            logging.debug("------CookieCheck----------")
            logging.debug("Tipo Sesion: " + str(idTipo))
            logging.debug("SESION: " + str(idSesion))
            logging.debug("Usuario: " + str(nombreUsuario))
            try:
                logging.debug("Ha caducado: " + str(sehaborrado))
            except UnboundLocalError:
                logging.debug("no hay cookies")
            #TEMP
            logging.debug("Sesiones Locales: " + str(UserHandler.listaSesiones))
            logging.debug("Sesiones OAUTH: " + str(OAuthHandler.listaSesiones))
            logging.debug("---------------------------")

            #Si el nombre de usuario es None, significa que la sesion ha
            #caducado o que no existe. Hay que hacer login.
            if nombreUsuario == None:
                logging.info("La sesión no existe o ha caducado."+
                "Por favor, inicie sesión.")
                response = make_response(redirect(url_for('blueUser.webLogin')))
                #Elimino cookies con datos de sesion como el umbral
                response.set_cookie('umbral', '', expires=0)
                return response
                #---
                #return redirect(url_for('blueUser.webLogin'))
            else:
                logging.debug("Sesión válida. Hola " + str(nombreUsuario))
    #You can handle 404s difeerently here if u want.
    else:
        #404
        logging.info("La pagina "+ request.path +" no existe. Redirigiendo...")
        return redirect(url_for('blueApp.webMain'))

"""
    GETTERS
"""

#Función utilizada en view functions para obtener el nombre del 
#usuario que está conectado. 
#Devolverá el nombre del usuario conectado o None si la sesión
#ha caducado o no existe.
#Similar a check_cookies() pero sin comprobar si las cookies han
#caducado.
def getCookieUserName(request):
    #Obtengo tipo de Cookie : local o OAuth
    idTipo=request.cookies.get('tipoLogin')
    #Obtengo valor Cookie
    idSesion=request.cookies.get('SessionId')
    #Inicializo nombreUsuario
    nombreUsuario=None
    if idTipo=="local":
        #Creo instancia del manjador de usuarios local
        UserHandler = UserManager()
        #Si la cookie ha caducado, me mostrara None como Usuario
        nombreUsuario = UserHandler.getCookieUserName(idSesion)
    elif idTipo=="oauth":
        #Creo instancia del manejador de usuarios OAuth
        OAuthHandler = OAuthUserManager()
        #Si la cookie ha caducado, me mostrara None como Usuario
        idUsuario = OAuthHandler.getCookieUserName(idSesion)
        nombreUsuario = OAuthHandler.getUserName(idUsuario)
    #DEBUG. Muesto info
    logging.debug("------getCookieUserName()----------")
    logging.debug("Tipo Sesion: " + str(idTipo))
    logging.debug("SESION: " + str(idSesion))
    logging.debug("Usuario: " + str(nombreUsuario))
    logging.debug("--------------------------------")

    return nombreUsuario

#Dada una petición (request), obtendremos de ella las cookies del cliente.
#De las mismas obtendremos el valot 'db', el cual contiene la base de datos que
#el cliente quiere emplear para sus consultas.
def getCookieDB(request):
    db = str(request.cookies.get('db'))

    logging.debug("------getCookieDB()----------")
    logging.debug("DB del cliente: ")
    if db == "MySQL":
        #Obtengo la instancia base de Flask para
        #poder pasarsela al constructor
        app = current_app._get_current_object()
        #retorno la instancia del manejador
        #de la base de datos de MySQL
        logging.debug("MySQL")
        #Actualizo las listas locales
        #para que contengan los números 
        #y las fechas actualizadas
        SQLHandler = sql_rnd.SQLHandler(app)
        SQLHandler.reload()
        return SQLHandler
    elif db == "Beebotte":
        #retorno la instancia del manejador
        #de la base de datos de Beebotte
        logging.debug("Beebotte")
        #Actualizo las listas locales
        #para que contengan los números 
        #y las fechas actualizadas
        BeeHandler = beebotte_rnd.BeeHandler()
        BeeHandler.reload()
        return BeeHandler
    elif db == "MongoDB":
        #retorno la instancia del manejador
        #de la base de datos de MongoDB
        logging.debug("MongoDB")
        #Actualizo las listas locales
        #para que contengan los números 
        #y las fechas actualizadas
        MongoHandler = mongo_rnd.MongoHandler()
        MongoHandler.reload()
        return MongoHandler
    #Valor por defecto: MongoDB (puede ser cualquiera)
    else:
        #retorno la instancia del manejador
        #de la base de datos por defecto.
        logging.debug("Desconocida")
        #Actualizo las listas locales
        #para que contengan los números 
        #y las fechas actualizadas
        MongoHandler = mongo_rnd.MongoHandler()
        MongoHandler.reload()
        return MongoHandler


