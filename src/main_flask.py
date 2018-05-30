# -*- coding: UTF-8 -*-
"""
EJEMPLO INICIAL DE FLASK
"""
#FLASK
from flask import Flask
#proceso para subir los datos a las BBDD
import rnd_uploader
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

##MONKEY PATCH
#Cuando cambiamos de página en el navegador, cerramos la 
#conexion SSE en esa página y abrimos otra cuando cargamos 
#la página  ala que vamos. Cuando el manejador de SSE envia
#un SSE a la primera conexion que esta cerrada, genera un error
#en el manejador de Django que anque capture en mi código sigue
#mostrando por la salida estandar el mensaje de error. La 
#siguiente función es para evitar que muestre por la salida estándar
#ese mensaje de error.
def patch_broken_pipe_error():
    """Monkey Patch BaseServer.handle_error to not write
    a stacktrace to stderr on broken pipe.
    http://stackoverflow.com/a/22618740/362702"""
    import sys
    from SocketServer import BaseServer
    from wsgiref import handlers

    handle_error = BaseServer.handle_error
    log_exception = handlers.BaseHandler.log_exception

    def is_broken_pipe_error():
        type, err, tb = sys.exc_info()
        return repr(err) == "error(32, 'Broken pipe')"

    def my_handle_error(self, request, client_address):
        if not is_broken_pipe_error():
            handle_error(self, request, client_address)

    def my_log_exception(self, exc_info):
        if not is_broken_pipe_error():
            log_exception(self, exc_info)

    BaseServer.handle_error = my_handle_error
    handlers.BaseHandler.log_exception = my_log_exception

patch_broken_pipe_error()

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
    tiempoSleep=5, debug = debug) 

    #Arrancar el servidor
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
    app.run(host='0.0.0.0', threaded=True)

    #señal de finalizar al proceso de subida de datos
    #uploader.enable = False
    uploader.finalizar()

    logging.debug("FIN")
