# -*- coding: UTF-8 -*-
#FLASK
from flask import Flask, render_template, url_for,\
redirect, request, make_response, Blueprint, current_app
#Usuarios en Bases de Datos
from mongo_user import UserManager
from mongo_oauth import OAuthUserManager
#importo en no_cookie_check
#necesario para evitar que me rediriga
#a la pantalla de login si no he iniciado
#sesion
from blue_cookie import no_cookie_check
#Log
import logging
from log_handler import setup_log, setStreamMode

blueUser = Blueprint('blueUser', __name__)

"""
  ____            _     _             
 |  _ \ ___  __ _(_)___| |_ _ __ ___  
 | |_) / _ \/ _` | / __| __| '__/ _ \ 
 |  _ <  __/ (_| | \__ \ |_| | | (_) |
 |_| \_\___|\__, |_|___/\__|_|  \___/ 
            |___/                     
"""
#Registro.
#Registro de usuarios de forma local. Los usuarios OAuth se
#registran el a ruta /jsoauthdata accesible desde 
#/jsoauthlogin.
#Obtenemos datos del cliente y creamos cuenta a partir
#de los mismos.
@blueUser.route("/register", methods=['GET','POST'])
@no_cookie_check
def webRegister():
    logging.debug("/register - METODO: " + str(request.method))

    #GET
    if request.method=='GET':
        return render_template("register.html")

    #POST
    if request.method=='POST':
        logging.debug("/register - Estoy en POST")
        username=str(request.form['username'])
        #username=request.args.get('username','default',type=str)
        password=str(request.form['password'])
        #password=request.args.get('password','default',type=str)
        umbral=float(request.form['umbral'])
        #username=request.args.get('umbral','101',type=float)

        #DEBUG
        cadena = '<html>REGISTRO:'
        cadena += '<br>usuario: ' + username
        cadena += '<br>password: ' + password
        cadena += '<br>umbral: ' + str(umbral)
        #Creo instancia del manejador de usuarios local
        UserHandler = UserManager()
        #Creacion usuario
        exito=UserHandler.createUser(username,password,umbral)
        cadena+='<br> RET: '+str(exito)+'</html>'
        logging.debug(cadena)
        #Le envio info sobre el resultado de la operacion y
        #la pagina web a donde hay que redirigir en caso de
        #craecion satisfactoria.
        #Este mensaje es interpretado por el cliente mediante javascript,
        #de forma que si exito==0 redirige a url_for('webLogin')
        return make_response(str(exito)+","+url_for('blueUser.webLogin'))

"""
  _                _       
 | |    ___   __ _(_)_ __  
 | |   / _ \ / _` | | '_ \ 
 | |__| (_) | (_| | | | | |
 |_____\___/ \__, |_|_| |_|
             |___/         
"""
#Login
@blueUser.route("/login", methods=['GET','POST'])
@no_cookie_check
def webLogin():
    if request.method == 'GET':
        return render_template("login.html")

    elif request.method == 'POST':
        #Los convierto a string pues estrán en tipo 'unicode'
        user=str(request.form['user'])
        #user=request.args.get('user','default',type=str)
        passw=str(request.form['pass'])
        #passw=request.args.get('pass','default',type=str)
        
        #DEBUG
        logging.debug("DEBUG - /login")
        logging.debug("user - type: " + str(type(user)))
        logging.info("user: " + str(user))
        logging.debug("pass - type: " + str(type(passw)))
        logging.info("pass: " + str(passw))

        #Creo la respuesta que devolveré al cliente.
        #Esta respuesta estrá compuesta por el resultado
        #devuelto por la función render_template().
        #A esta respuesta le añadiré la cookie generada como resultado del 
        #inicio de sesión, si este es satisfactorio.
        resp = make_response(redirect(url_for('blueApp.webMain')))

        #Creo instancia del manejador de usuarios local
        UserHandler = UserManager()
        #Obtengo cookie resultado de log in
        cookieVal=UserHandler.login(user,passw)
        #Si se ha iniciado sesion, el valor de 
        #cookieVal será != -1
        logging.debug("DEBUG - Cookie: " + str(cookieVal))
        if cookieVal >= 0:
            resp.set_cookie('SessionId', cookieVal)
            resp.set_cookie('tipoLogin', 'local')
            #también pongo umbral en la cookie, para notificaciones
            nombreUsuario = UserHandler.getCookieUserName(cookieVal)
            umbralUsuario = UserHandler.getUmbral(nombreUsuario)
            logging.debug(">>>>>>>>>>>>UMBRAL USUSARIO: " + str(umbralUsuario))
            resp.set_cookie('umbral', str(umbralUsuario))
            
        #return redirect(url_for('blueApp.webMain'))
        return resp

"""
  _                            _   
 | |    ___   __ _  ___  _   _| |_ 
 | |   / _ \ / _` |/ _ \| | | | __|
 | |__| (_) | (_| | (_) | |_| | |_ 
 |_____\___/ \__, |\___/ \__,_|\__|
             |___/                 
"""

#Logout
@blueUser.route("/logout")
def webLogout():
    #Obtengo info de las cookies
    idSesion=request.cookies.get('SessionId')
    #tipo de login
    idTipo=request.cookies.get('tipoLogin')
    #OAUTH
    if idTipo=="oauth":
        #Creo instancia del manejador de usuarios OAuth
        OAuthHandler = OAuthUserManager()
        #Logout al usuario
        logging.info("(OAuth)logging out user: " + idSesion)
        OAuthHandler.logout(idSesion)
    #LOCAL
    elif idTipo=="local":
        logging.info("(Local)logging out user: " + idSesion)
        #Creo instancia del manejador de usuarios local
        UserHandler = UserManager()
        #Logout al usuario
        UserHandler.logout(idSesion)

    #Retornamos a la pag de login
    response=make_response(redirect(url_for('blueUser.webLogin')))
    #Borramos datos cookies
    response.set_cookie('umbral', '', expires=0)
    return response
    

"""
  _   _           _               _ 
 | | | |_ __ ___ | |__  _ __ __ _| |
 | | | | '_ ` _ \| '_ \| '__/ _` | |
 | |_| | | | | | | |_) | | | (_| | |
  \___/|_| |_| |_|_.__/|_|  \__,_|_|
                                    
"""
#CAMBIAR umbral del usuario
@blueUser.route('/cambiarUmbral', methods=['GET','POST'])
def cambiarUmbral():
    logging.debug("/cambiarUmbral - METODO: " + str(request.method))
    response = make_response("cambiarUmbral_placeholder")
    #Obtengo info de las cookies
    idSesion=request.cookies.get('SessionId')
    #tipo de login
    idTipo=request.cookies.get('tipoLogin')
    #inicio variables en caso de que no haya cookies en el cliente
    nombreUser=None
    nombreAMostrar=None
    #Creo instancia del manejador de usuarios local
    UserHandler = UserManager()
    #Creo instancia del manejador de usuarios OAuth
    OAuthHandler = OAuthUserManager()
    #OAUTH
    if idTipo=="oauth":
        nombreUser=OAuthHandler.getCookieUserName(idSesion)
        nombreAMostrar=OAuthHandler.getUserName(nombreUser)
    #LOCAL
    elif idTipo=="local":
        nombreUser=UserHandler.getCookieUserName(idSesion)
        nombreAMostrar=nombreUser
    #-------
    #GET
    if request.method == 'GET':
        response = render_template('changeUserUmbral.html',
        username=nombreAMostrar)

    #POST
    elif request.method == 'POST':
    #else:
        logging.debug("Estoy en POST")
        
        #umbral=request.form['umbral']
        umbral=request.form.get('umbral',101)
        #umbral = request.args.get('umbral', 101, type=float)
        #
        #resquest.args.get es mucho mejor, si no encuentra el argumento
        #'umbral' en vez de lanzar una excepcion da un valor por defecto,
        #el cual podemos especificar, asi como su tipo.
        #
        #INCORRECTO. request.args.get se emplea cuando se envian
        #parametros mediante GET (los cuales estarán incluidos en la
        #url).
        #Lo que es mejor que request.form[<nombreParam>] es 
        #request.form.get(<nombreParam>, defaultValue), ya que de 
        #esta forma, si no estan los parametros que intentamos
        #obtener, la funcion nos devolverá el valor por defecto
        #especificado en vez de 'None'.
        logging.debug("UMBRAL RECIBIDO: " + str(umbral))
        logging.debug("tipo: " + str(type(umbral)))
        try:
            umbral=float(umbral)
        except ValueError:
            umbral=101
        #CAMBIO UMBRAL DEL USUARIO.
        if idTipo=="oauth":
            OAuthHandler.modUmbral(nombreUser, umbral)
            #response=make_response("UMB:"+str(OAuthHandler.getUmbral(nombreUser)))
            umbralDef = OAuthHandler.getUmbral(nombreUser)
            response=make_response("UMB:"+str(umbralDef))
        elif idTipo=="local":
            UserHandler.modUmbral(nombreUser, umbral)
            #response=make_response("UMB:"+str(UserHandler.getUmbral(nombreUser)))
            umbralDef = UserHandler.getUmbral(nombreUser)
            response=make_response("UMB:"+str(umbralDef))
        else:
            #EL usuario no ha hecho login.
            #
            #Los codigos de error de getUmbral() son:
            #-> 102: El usuario es 'None'. Es el valor que se obtiene cuando no se ha
            #iniciado sesión
            #-> 103: Indica que el nombre de usuario recibido no es válido, ya sea por tipo
            #(no string) o longitud.
            #-> 104: El usuario indicado no se ha encontrado en la base de datos.
            #
            #Los respuestas que se pueden obtener de modUmbral() van de -100
            #a 104, invluyendo todos los códigos de error. Para indicar
            #es error que es que no se ha iniciado sesión, utilizaremos el
            #código 105.
            #response=make_response("Inicia sesión antes de cambiar umbral.")
            umbralDef = 105
            response=make_response("UMB:"+str(umbralDef))
            #Los códigos de error los interpretaremos en el cliente 
        #response=make_response(str(umbral))
        #Almaceno informacion del umbral en las cookies
        logging.debug(">>>>>>>>>>>>UMBRAL USUARIO: " + str(umbralDef))
        response.set_cookie('umbral', str(umbralDef))
    return response


"""
     _                             _   
    / \   ___ ___ ___  _   _ _ __ | |_ 
   / _ \ / __/ __/ _ \| | | | '_ \| __|
  / ___ \ (_| (_| (_) | |_| | | | | |_ 
 /_/   \_\___\___\___/ \__,_|_| |_|\__|
                                       
"""
#Mostrar la informacion del usuario y permitir 
#cambiar el umbral y hacer logout
@blueUser.route('/cuenta')
def webAccount():
    #Obtengo info de usuario
    #Obtengo info de las cookies
    idSesion=request.cookies.get('SessionId')
    #tipo de login
    idTipo=request.cookies.get('tipoLogin')

    #Creo instancia del manejador de usuarios local
    UserHandler = UserManager()
    #Creo instancia del manejador de usuarios OAuth
    OAuthHandler = OAuthUserManager()
    
    #Incializamos vairables
    userid = None
    nombre = None
    email = None
    proveedor = None
    umbral = None

    #OAUTH
    if idTipo=="oauth":
        #Obtengo informacion Usuario OAuth
        userid = OAuthHandler.getCookieUserName(idSesion)
        nombre = OAuthHandler.getUserName(userid)
        email = OAuthHandler.getUserMail(userid)
        proveedor = OAuthHandler.getUserProvider(userid)
        umbral = OAuthHandler.getUmbral(userid)
    #LOCAL
    elif idTipo=="local":
        #Obtengo información Usuario Local
        userid = UserHandler.getCookieUserName(idSesion)
        nombre = userid
        umbral = UserHandler.getUmbral(nombre)

    #LLegados a este punto, si userid == None, una de dos:
    #o el usuario tiene cookie de sesion y le ha caducado,
    #o directamente no tiene cookie de sesion.
    #La forma de proceder en ambos casos es hacer que el
    #cliente inicie sesión en la aplicacion, por lo que
    #le redirigiremos a la pagina de login.
    if userid==None:
        #Creo respuesta
        response = make_response(redirect(url_for('blueUser.webLogin')))
    
    #En caso contrario, obtenemos los datos y los devolvemos
    else:
        #Creo respuesta
        response = make_response(render_template("accountInfo.html",\
        nombrehtml = nombre, emailhtml = email,\
        proveedorhtml=proveedor, umbralhtml=umbral,\
        tipoRegistrohtml = idTipo))

    #Retorno la respuesta
    return response
    
