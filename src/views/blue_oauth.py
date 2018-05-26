# -*- coding: UTF-8 -*-
#FLASK
from flask import Flask, render_template, url_for,\
redirect, request, make_response, Blueprint, current_app
#Usuarios en Bases de Datos
from mongo_oauth import OAuthUserManager
#importo en no_cookie_check
#necesario para evitar que me rediriga
#a la pantalla de login si no he iniciado
#sesion
from blue_cookie import no_cookie_check
#Log
import logging
from log_handler import setup_log, setStreamMode

"""
   ___    _         _   _     
  / _ \  / \  _   _| |_| |__  
 | | | |/ _ \| | | | __| '_ \ 
 | |_| / ___ \ |_| | |_| | | |
  \___/_/   \_\__,_|\__|_| |_|
                              
"""

blueOAuth = Blueprint('blueOAuth', __name__)

#Obtiene ClientId de el fichero correspondiente en ./credentials
def getClientId():
    import json
    try:
        json_data = open("credentials/google_api_data.json")
        data = json.load(json_data)
        ClientId = str(data['web']['client_id'])
        logging.info("ID GOOGLE: " + ClientId)
    except IOError:
        logging.warning("NO SE HA PODIDO ABRIR ARCHIVO CREDENCIALES!!!!!!!!")
        ClientId="ERROR"
    return ClientId

#LOGIN por OAuth de Google
@blueOAuth.route("/jsoauthlogin/")
@no_cookie_check
def jsOAuthLogin():
    # Specify the CLIENT_ID of the app that accesses the backend:
    #nemrod962@gmail.com
    #CLIENT_ID="933060102795-0hf4m6v3cuq4ocvubaide7ouqui2l4lg.apps.googleusercontent.com"
    #randomlender@gmail.com
    #CLIENT_ID="324401899197-2cag1rbuoium6s2q96m1i0hm3fjium4g.apps.googleusercontent.com"
    CLIENT_ID=getClientId()
    return render_template("jsoauthlogin.html",id_api=CLIENT_ID)

#VERIFICAR datos e iniciar sesion
@blueOAuth.route("/jsoauthdata/", methods=['POST'])
@no_cookie_check
def jsOAuthData():
    #Creo instancia del manejador de usuarios OAuth
    OAuthHandler = OAuthUserManager()
    #Obtener datos enviados por cliente.
    token=request.form['idtoken']
    #token=request.get.args('idtoken','placeholder',type=str)
    logging.info("RECIBIDO - token:" + str(token))

    #-----VALIDACION TOKEN
    from google.oauth2 import id_token
    from google.auth.transport import requests
    # Specify the CLIENT_ID of the app that accesses the backend:
    #nemrod962@gmail.com
    #CLIENT_ID="933060102795-0hf4m6v3cuq4ocvubaide7ouqui2l4lg.apps.googleusercontent.com"
    #randomlender@gmail.com
    #CLIENT_ID="324401899197-2cag1rbuoium6s2q96m1i0hm3fjium4g.apps.googleusercontent.com"
    CLIENT_ID=getClientId()
    try:
        #Toda la informacion en diccionario idinfo
        idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
        #Diversas variables relevantes en mi caso
        userid = str(idinfo['sub'])
        usermail = str(idinfo['email'])
        username =  str(idinfo['name'])
        userprov = str(idinfo['iss'])
        #mostramos variables
        logging.debug("USERID: " + userid)
        logging.debug("USERMAIL: " + idinfo['email'])
        logging.debug("NAME: " + idinfo['name'])
        logging.debug("PROVEEDOR" + idinfo['iss'])
        logging.debug("mas info?: ")
        logging.debug("data: " + str(idinfo))
        logging.debug("tipo: " + str(type(idinfo)))
    except ValueError as e:
        logging.warning("ERROR TOKEN: " + str(e))
        #Error con el token recibido, no
        #es valido. Redirigo a la pagina login
        return redirect(url_for('blueUser.webLogin'))
        #Puede enviarse un idtoken arbitrario con
        #curl --data "idtoken=value1" dominioppr.com:5000/jsoauthdata/
        #Esto será manjado mediante este error.


    #-----
    #Trabajando con usuario

    #EXISTE?
    existe=OAuthHandler.checkUserName(userid)
    if existe:
        logging.debug("Usuario " + userid + " existe!")
    else:
        #SI NO EXISTE -> LO CREAMOS
        logging.info("Usuario " + userid + " NO existe.")
        logging.info("Creando...")
        #umbral 101 por defecto
        userumbral=101
        r=OAuthHandler.createUser(userprov, userid, usermail, username, userumbral)
        logging.debug("ATENCION:")
        logging.debug("db: " + str(OAuthHandler.client))
        logging.debug("res " + str(r))
        #print "res>0 : " + str(r>0)
        if r > 0:
            logging.debug("Usuario " + username + " creado!")
        else:
            logging.warning("Error al crear usuario: " + username)
            #Error -2 -> Mal formato argumentos de createUser().
            #Error -1 -> Usuario ya existe.
            logging.warning("Error: " + str(r))
            #Que hago en este caso? Nada?
            mensajeError= "Error al crear usuario (ERROR: "+str(r)+ "): "
            if r == -2:
                mensajeError += "Mal formato argumentos de createUser()."
            if r == -1:
                mensajeError += "Usuario ya existe."
            return make_response(mensajeError)
    
    #CREAR COOKIE, independientemenste de si existia el usuario o no.
    #Llegados a este punto, tendremos el usuario creado en la
    #base de datos de MongoDB.
    #Ahora iniciamos la sesion, para lo que tendremos que crear las cookies

    #Obtengo valor de la cookies. 
    cookieVal = OAuthHandler.login(userid)
    logging.debug("DEBUG - Cookie: " + str(cookieVal))
    #creo la cookie si el valor que me ha devuelto es válido (> 0).
    #login devolverá -1 si el usuario no existe o -2 si userid
    #no es del tipo 'string'.
    if cookieVal > 0:
        #Si hemos creado el usuario, tenemos que ofrecerle
        #que especifique su umbral.
        if not existe:
            response = make_response(url_for('blueUser.cambiarUmbral'))
        #Si ya existía, lo redirigimos al menú principal
        else:
            response = make_response(url_for('blueApp.webMain'))
        #Asignamos los datos de la cookie creada a la respuesta
        response.set_cookie('SessionId', cookieVal)
        response.set_cookie('tipoLogin', 'oauth')
        #también pongo umbral en la cookie, para notificaciones
        nombreUsuario = OAuthHandler.getCookieUserName(cookieVal)
        umbralUsuario = OAuthHandler.getUmbral(nombreUsuario)
        logging.debug(">>>>>>>>>>>>UMBRAL USUSARIO: " + str(umbralUsuario))
        response.set_cookie('umbral', str(umbralUsuario))
    else:
        #Si ha habido error al hacer login, redirigimos a la pagina de 
        #login
        #response = make_response(url_for('webLogin'))
        logging.warning("PELIGRO! ERROR AL HACER LOGIN en /jsoauthdata/")
        response = make_response(url_for('blueApp.webMain'))

    #Retornamos la respuesta creada.
    return response

    #-----
    #No debería llegar a ejecutarse este return
    return "RECIBIDO - token:" + str(request.form['idtoken'])
    #return redirect(url_for('webMain'))

    
