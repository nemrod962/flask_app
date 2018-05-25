# -*- coding: UTF-8 -*-
"""
EJEMPLO INICIAL DE FLASK
"""
#FLASK
from flask import Flask, render_template, url_for,\
redirect, request, make_response, Blueprint
#Clase encargada de crear SSE y
#enviarlos a los suscriptores.
from sse_handler import SSEHandler
#importo en no_cookie_check
#necesario para evitar que me rediriga
#a la pantalla de login si no he iniciado
#sesion
from blue_cookie import no_cookie_check

"""
  ____                             ____             _     _____                 _       
 / ___|  ___ _ ____   _____ _ __  / ___|  ___ _ __ | |_  | ____|_   _____ _ __ | |_ ___ 
 \___ \ / _ \ '__\ \ / / _ \ '__| \___ \ / _ \ '_ \| __| |  _| \ \ / / _ \ '_ \| __/ __|
  ___) |  __/ |   \ V /  __/ |     ___) |  __/ | | | |_  | |___ \ V /  __/ | | | |_\__ \
 |____/ \___|_|    \_/ \___|_|    |____/ \___|_| |_|\__| |_____| \_/ \___|_| |_|\__|___/
                                                                                        
"""

blueSSE = Blueprint('blueSSE', __name__)

#El cliente se conectará a esta ruta para registrarse y que 
#el servidor le envíe los SSE.
@blueSSE.route('/sse')
@no_cookie_check
def webSSE():
    sseHandler = SSEHandler()
    return sseHandler.sendSSE()

#test
@blueSSE.route('/send')
@no_cookie_check
def sendTest():
    sseHandler = SSEHandler()
    return sseHandler.createSSE()

@blueSSE.route('/send/<msg>')
@no_cookie_check
def sendTest2(msg):
    sseHandler = SSEHandler()
    return sseHandler.createSSE(msg)

