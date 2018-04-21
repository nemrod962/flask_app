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
#Crear Graficas
import graph_maker
#Graficas plot.ly
import plotly_manager

#Creo instancia de Flask
app = Flask(__name__) 

#VAR GLOBAL
#debug - Activar si se quieren ver los mensajes
#debug = False
#Manejo de BBDD
SQLHandler = sql_rnd.SQLHandler(app)
BeeHandler = beebotte_rnd.BeeHandler()
MongoHandler = mongo_rnd.MongoHandler()

#Manejo de Usuarios almacenados en MongoDB
UserHandler = UserManager()

#Manejador a emplear. Será elegido en el
#menú principal. Por defecto Beebotte.
#DBHandler = SQLHandler
DBHandler = MongoHandler

#Cargo en en las listas globales de DBHandler
#los datos de las bases de datos inicialmente,
#de forma que cuando acceda al menú principal por
#primera vez las listas ya estén pobladas
DBHandler.reload()

#TESTOAUTH
@app.route("/testoauth/")
def testoauth():
    from myoauth.my_google_oauth import OAuthHandler
    from myoauth.my_google_oauth import OAuthRes
    oa = OAuthHandler(app)
    
    d=OAuthRes()
    res= oa.getOAuthCredentials(d)
    print "testing: " + str(res)
    print "type_ " + str(type(res))
    try:
        print "DICT testing: " + str(d)
        print "DICT testing: " + str(any(d))
        print "type_ " + str(type(d))
        print "type_ " + str(d.getDataType)
    except:
        print ""
    return res
    
    #print "ATENCION" + str(oa.wrapPollo())
    #return redirect(url_for('webMain'))


#PAGINA INICIAL
#Login
@app.route("/login")
def webLogin():
    return render_template("login.html")

@app.route("/login", methods=['POST'])
def webLogin_post():
    #Los convierto a string pues estrán en tipo 'unicode'
    user=str(request.form['user'])
    passw=str(request.form['pass'])
    
    #DEBUG
    print "DEBUG - /login"
    print "user - type: " + str(type(user))
    print "user: " + str(user)
    print "pass - type: " + str(type(passw))
    print "pass: " + str(passw)

    #Creo la respuesta que devolveré al cliente.
    #Esta respuesta estrá compuesta por el resultado
    #devuelto por la función render_template().
    #A esta respuesta le añadiré la cookie generada como resultado del 
    #inicio de sesión, si este es satisfactorio.
    resp = make_response(redirect(url_for('webMain')))

    #Obtengo cookie resultado de log in
    cookieVal=UserHandler.login(user,passw)
    #Si se ha iniciado sesion, el valor de 
    #cookieVal será != -1
    print "DEBUG - Cookie: " + str(cookieVal)
    if cookieVal != -1:
        resp.set_cookie('SessionId', cookieVal)
    
    #return redirect(url_for('webMain'))
    return resp


#menú principal
#Mostramos la pagina inicial
@app.route("/") 
def webMain():

    #Cookies
    #Obtengo Cookie
    idSesion=request.cookies.get('SessionId')
    #CADUCIDAD - BORRO Y ACTUALIZO
    UserHandler.checkCookieStatus(idSesion)
    #Muesto info
    print "SESION: " + str(idSesion)
    #Si la cookie ha caducado, me mostrara None como Usuario
    nombreUsuario = UserHandler.getCookieUserName(idSesion)
    print "Usuario: " + str(nombreUsuario)
    #---
    return render_template("index.html",\
    DBName = web_functions.getDBName(DBHandler))

#Procesamos la opción elegida en la pagina inicial
@app.route("/", methods=['POST'])
def webMain_post():
    opcion = request.form['option']

    umbraltxt = request.form['umbralTxt']
    if debug:
        print "--->"+umbraltxt
        
    
    #Dependiendo de la direccion seleccionada en
    #la pantalla inicial redirigiremos a una dirección 
    #o a otra.
    if opcion == "elegir":
        return redirect(url_for('webDBSelect'))

    if opcion == "tablas":
        #return redirect(url_for('show_type', sensor="s1"))
        return redirect(url_for('webTabla'))
    """
    if opcion == "umbral":
        return redirect(url_for('webUmbral'))
    """
    if opcion == "umbral":
        #Evitar cadena vacia
        if umbraltxt == "":
            umbraltxt = "error"
        return redirect(url_for('webUmbral', umb = umbraltxt))

    if opcion == "media":
        return redirect(url_for('webMedia'))

    if opcion == "grafoBee":
        return redirect(url_for('webGrafoBee'))

    if opcion == "grafo":
        return redirect(url_for('createGraph'))

    if opcion == "plotly":
        #return redirect(url_for('plotly'))
        plotlyHandler=plotly_manager.PlotlyHandler()
        plotlyHandler.crearGrafo(DBHandler)
        #Abre la gráfica en una nueva pestaña
        #del navegador, por lo que vuelvo a 
        #cargar el menú principal. No necesito
        #cargar otra paǵina.
        return redirect(url_for('webMain'))

    else:
        return "ERROR: Opción Desconocida"

#ELEGIR DB
@app.route("/seleccDB")
def webDBSelect():
    return render_template("DBselect.html")

@app.route("/seleccDB", methods=['POST'])
def webDBSelect_post():
    opcion = request.form['chosenDB']
    #Declaro DBHandler como global para que
    #su valor realmente cambie en todo el programa,
    #no solo dentro de esta funcion.
    global DBHandler
    if debug:
        print "---"+opcion+"---"
    if opcion == "MySQL":
        DBHandler = SQLHandler
    elif opcion == "Beebotte":
        DBHandler = BeeHandler
    elif opcion == "MongoDB":
        DBHandler = MongoHandler
    else:
        print "DB seleccionada descon."
    #Una vez seleccionada la base de datos,
    #utilizo la funcion reload() para que 
    #pueble las listas globales con los numeros
    #aleatorios y su fecha de obtencion
    DBHandler.reload()
    #return render_template("DBselect.html")
    return redirect(url_for('webMain'))

#TABLAS
@app.route("/tablas")
def webTabla():
    #return "Tablas: PLACEHOLDER"
    return render_template("tablas.html",\
    tablaHTML = web_presentation.getTableHTML(DBHandler, debug),\
    DBName = web_functions.getDBName(DBHandler))

@app.route("/tablas", methods=['POST'])
def webTabla_post():
    return redirect(url_for('webMain'))

#UMBRAL
@app.route("/umbral/<umb>")
def webUmbral(umb):
    #return "Umbral: PLACEHOLDER"
    try:
        trueUmbral = float(umb)
    except ValueError:
        if debug:
            print "NO SE HA INTRODUCIDO NUMERO COMO UMBRAL!"
        umb = "Debe introducirse un numero. Usando valor por defecto: 50."
        trueUmbral = 50
    if debug:
        print "str: " + umb
        print "float: " + str(trueUmbral)
    return render_template("umbral.html",\
    umbralHTML = umb,\
    resUmbral = web_presentation.getUmbralHTML(DBHandler, trueUmbral , debug),\
    DBName = web_functions.getDBName(DBHandler))
    #resUmbral = "<div>HOLA</div>")

@app.route("/umbral", methods=['POST'])
def webUmbral_post():
    return redirect(url_for('webMain'))


#MEDIA
@app.route("/media")
def webMedia():
    #return "Media: PLACEHOLDER"
    return render_template("media.html",\
    resMedia = web_presentation.getMediaHTML(DBHandler, debug),\
    DBName = web_functions.getDBName(DBHandler))

@app.route("/media", methods=['POST'])
def webMedia_post():
    return redirect(url_for('webMain'))

#GRAFOS REMOTOS (obtenidos de Beebotte)
@app.route("/grafoBee")
def webGrafoBee():
    #return "Grafo: PLACEHOLDER"
    return render_template("grafoBee.html",\
    resGrafo = web_presentation.getGrafoHTML(debug))

@app.route("/grafoBee", methods=['POST'])
def webGrafoBee_post():
    return redirect(url_for('webMain'))

#GRAFOS LOCALES, los creo con la clase GraphMaker en graph_maker.py
@app.route("/grafo")
def createGraph():
    
    #Las urls pueden tener las dos siguientes formas:
    #http://0.0.0.0:5000/grafo
    #http://0.0.0.0:5000/grafo?tipo=line
    #Para obtener el valor del argumento tipo en la segunda
    #url emplearemos la siguiente línea de código.
    tipo = request.args.get('tipo')
    #En caso de que la url recibida sea del primer tipo
    #y no contenga parámetros, el valor de tipo será 'None'
    #print "argumento URL: " + str(tipo)

    #creo instancia
    gm = graph_maker.GraphMaker()
    
    #return gm.crearGrafo(DBHandler)
    
    return render_template("grafo.html",\
    nombreDBSimple=web_functions.getDBSimpleName(DBHandler),\
    graph_data=gm.crearGrafo(DBHandler, tipo),\
    DBName = web_functions.getDBName(DBHandler))


@app.route("/grafo", methods=['POST'])
def createGraph_post():
    #obtener datos del form
    try:
        tipoGrafo = request.form['graphType']
    except:
        #print "Has pulsado volver al menu principal."
        #Este código se ejecuta cuando se selecciona volver
        #al menú principal en lugar de seleccionar el tipo
        #de lista. Supongo que esto es debido a que si
        #pulsamos el botón volver al menú principal, se esta utilizando
        #el formulario 'volver', por lo que el formulario 'graphType' no 
        #tiene ningún valor y da error al obtenerlo.

        #Si se ha pulsado el botón 'volver al menú principal', pues
        #redirigimos a la página principal
        return redirect(url_for('webMain'))
    try:
        volver = request.form['volver']
    except:
        #print "Has pulsado Refresh."
        #Este código se ejecuta cuando se selecciona el tipo de
        #lista. Supongo que esto es debido a que si seleccionamos
        #el tipo de lista, estamos devolviendo el valor del formulario 
        #'graphType', por lo que el formulario 'volver' (el botón para
        #volver al menú principal) no tiene ningún valor y da error al obtenerlo.
        
        #Si se ha seleccionado 'Refresh', volvemos a cargar la página del grafo
        #con le tipo de grafo indicado.

        #Hay dos formas de que createGraph lea este argumento 'arg'.
        #   1º -> Si en la url de createGraph hay un argumento 'arg', la
        #funcion recibira arg como parámetro y podemos leerlo directamente.
        #Podemos también utilizar rutas opcionales para que createGraph
        #necesite este argumento en su url o no:
        #@app.route("/grafo/")
        #@app.route("/grafo/<arg>")
        #def createGraph(arg=None):
        #    print "argumento: " + str(arg)
        #
        #   2º -> Otra forma es incluir este argumento como un argumento
        #en la propia url. Dentro de la función podemos leer este argumento
        #de la url de la siguiente forma:
        #@app.route("/grafo")
        #def createGraph():
        #    arg = request.args.get('arg')
        #    print "argumento URL: " + str(arg)
        #
        #La ventaja de este segundo metodo es que no tenemos que definir urls
        #opcionales para la función como en el caso anterior.
        return redirect(url_for('createGraph', tipo=tipoGrafo))

    #No se debería llegar a este punto, pero por si se llega
    #redirigimos al menú principal.
    return redirect(url_for('webMain'))

if __name__ == "__main__":

   #Pregunto si se quiere activar al modo debug
   global debug
   
   debug_str = raw_input("Activar Modo Debug?[Y\N]: ")
   
   if debug_str == "Y" or debug_str == "y":
       debug = True
   else:
       debug = False


   #Iniciar y lanzar proceso de carga de datos en las BBDD
   #LOS MANEJADORES DE LAS DBs SE INICIALIZAN EN SU CONSTRUCTOR
   uploader = rnd_uploader.RndUploader(app, SQLHandler, BeeHandler,\
   MongoHandler,120, debug) 
   
   #prueba de las funcionalidades
   if debug:
       r1 = web_functions.umbral(uploader.getSQLHandler(), 50, True) 
       r2 = web_functions.umbral(uploader.getBeeHandler(), 50, True) 
       r3 = web_functions.umbral(None, 50) 
       media1 = web_functions.media(uploader.getSQLHandler(), True)
       media2 = web_functions.media(uploader.getBeeHandler(), True)
       print "---"
       print "r1: "
       print r1
       print "r2: "
       print r2
       print "r3: "
       print r3
       print "media SQL: "
       print media1
       print "media Bee: "
       print media2
   
   
   #Arrancar el el servidor
   app.run(host='0.0.0.0')

    
   #señal de finalizar al proceso de subida de datos
   #uploader.enable = False
   uploader.finalizar()

   print "FIN"
