# -*- coding: UTF-8 -*-
"""
EJEMPLO INICIAL DE FLASK
"""
#FLASK
from flask import Flask, render_template, url_for,\
redirect, request, make_response
#proceso para subir los datos a las BBDD
import rnd_uploader
#funcionalidad de la web con los datos
import web_functions
import web_presentation
#Manejo Bases de Datos
import sql_rnd
import beebotte_rnd
import mongo_rnd
#Usuarios en Bases de Datos
from mongo_user import UserManager
from mongo_oauth import OAuthUserManager
#Crear Graficas
import graph_maker
#Graficas plot.ly
import plotly_manager
#gevent. Para lanzar la aplicación
#en varios procesos. Uno de ellos se 
#encargará de manejar y enviar los
#sse (server side events).
#En lugar de emplear app.run(),
#se usará la clase WSGIServer
from gevent.pywsgi import WSGIServer
#Clase encargada de crear SSE y
#enviarlos a los suscriptores.
from sse_handler import SSEHandler
#Threading
from threading import Thread
#Log
import logging
from log_handler import setup_log, setStreamMode
#Vistas
from views.blue_cookie import blueCookie,\
no_cookie_check, getCookieUserName, getCookieDB
from views.blue_sse import blueSSE
from views.blue_oauth import blueOAuth
from views.blue_user import blueUser
from views.blue_app import blueApp
from views.legacy.blue_legacy_app import blueLegacyApp
#---
#Log
setup_log()
#Creo instancia de Flask
app = Flask(__name__) 
#Agrego Blueprints (vistas)
app.register_blueprint(blueCookie)
app.register_blueprint(blueSSE)
app.register_blueprint(blueOAuth)
app.register_blueprint(blueUser)
app.register_blueprint(blueApp)
app.register_blueprint(blueLegacyApp, url_prefix='/legacy')


#VAR GLOBAL
#debug - Activar si se quieren ver los mensajes
#debug = False
#Manejo de BBDD
#SQLHandler = sql_rnd.SQLHandler(app)
#BeeHandler = beebotte_rnd.BeeHandler()
#MongoHandler = mongo_rnd.MongoHandler()

#Manejo de Usuarios almacenados en MongoDB
#UserHandler = UserManager()
#Usuarios OAuth
#OAuthHandler = OAuthUserManager()

#Encargado de manejar los SSE
#sseHandler = SSEHandler()

#DEPRECATED - Guardar Manejador preferido en cookies de cliente.
#Manejador a emplear. Será elegido en el
#menú principal. Por defecto Beebotte.
#DBHandler = SQLHandler
#DBHandler = MongoHandler
#DBHandler = BeeHandler
#
#Cargo en en las listas globales de DBHandler
#los datos de las bases de datos inicialmente,
#de forma que cuando acceda al menú principal por
#primera vez las listas ya estén pobladas
#DBHandler.reload()

#Muestra por la salida estandar una vista de las direcciones
#disponibles en la aplicación
@app.route('/map')
@no_cookie_check
def site_map():
	import urllib
	output = []
	for rule in app.url_map.iter_rules():
		options = {}
		for arg in rule.arguments:
			options[arg] = "[{0}]".format(arg)

		methods = ','.join(rule.methods)
		url = url_for(rule.endpoint, **options)
		line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
		output.append(line)

	for line in sorted(output):
		print line
	return str(output)
    
if __name__ == "__main__":

    #Pregunto si se quiere activar al modo debug
    global debug

    debug_str = raw_input("Activar Modo Debug?[Y\N]: ")

    if debug_str == "Y" or debug_str == "y":
       debug = True
    else:
       debug = False

    if debug:
        setStreamMode(logging.DEBUG)

    logging.debug("INIT")

    #Iniciar y lanzar proceso de carga de datos en las BBDD
    #LOS MANEJADORES DE LAS DBs SE INICIALIZAN EN SU CONSTRUCTOR
    uploader = rnd_uploader.RndUploader(flaskApp = app,\
    tiempoSleep=30, debug = debug) 

    #Arrancar el el servidor
    #app.run(host='0.0.0.0')

    #IMPORTANTE. ES NECESARIO EMPLEAR WGSISserver de gevent
    #para lanzar la aplicación.
    #Al emplear SSE, vamos a necesitar un proceso que se encargue
    #de estar trabajando con la cola de SSEs todo el tiempo.
    #SI no ejecutamos la aplicación mediante varios procesos (usando
    #gevent.WGSIServer), el único proceso de la aplicación se quedará 
    #trabajando con esta cola de SSE y no podrá atender al cliente.
    #
    #UPDATE: es necesario emplear threaded=True en app.run en vez de
    #WSGIServer, ya que este último no ofrece el rendimiento apropiado
    #(se traba si hay más de dos conexiones por parte del cliente).
    """
    server = WSGIServer(("0.0.0.0", 5000), app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logging.info("Terminado por el usuario")
    """
    app.run(host='0.0.0.0', threaded=True)

    #señal de finalizar al proceso de subida de datos
    #uploader.enable = False
    uploader.finalizar()

    logging.debug("FIN")
