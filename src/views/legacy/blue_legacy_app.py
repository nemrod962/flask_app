# -*- coding: UTF-8 -*-
#FLASK
from flask import Flask, render_template, url_for,\
redirect, request, make_response, Blueprint, current_app
#Librerias requeridas por Legacy
#plotly
import plotly_manager
#pygal
import graph_maker
#genera html a partir de datos
import web_presentation
#Obtiene nombres de la base de datos empleada
from db_name_getter import getDBName, getDBSimpleName
#Log
import logging
from log_handler import setup_log
#Views
#import sys
#necesario ya que las views estan en la carpeta superior
#sys.path.append('../')
from views.blue_cookie import getCookieUserName, getCookieDB

blueLegacyApp = Blueprint('blueLegacyApp', __name__,\
template_folder='legacy_templates')


"""
  _                                  ____             _            
 | |    ___  __ _  __ _  ___ _   _  |  _ \ ___  _   _| |_ ___  ___ 
 | |   / _ \/ _` |/ _` |/ __| | | | | |_) / _ \| | | | __/ _ \/ __|
 | |__|  __/ (_| | (_| | (__| |_| | |  _ < (_) | |_| | ||  __/\__ \
 |_____\___|\__, |\__,_|\___|\__, | |_| \_\___/ \__,_|\__\___||___/
            |___/            |___/                                 
"""
#menú principal VIEJO
#Mostramos la pagina inicial VIEJA
@blueLegacyApp.route("/") 
def webMain():

    nombreUsuario = getCookieUserName(request)
    #Obtengo el manejador de la BD a 
    #utilizar según la cookie del usuario.
    DBHandler = getCookieDB(request)
    logging.debug("MAIN: Usuario - " + str(nombreUsuario))
    #---
    response = make_response(render_template("index.html.old",\
    DBName = getDBName(DBHandler),\
    username=nombreUsuario))

    #if sehaborrado:
    #    response.set_cookie('expired','1')
    return response

#Procesamos la opción elegida en la pagina inicial Vieja
@blueLegacyApp.route("/", methods=['POST'])
def webMain_post():
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
        return redirect(url_for('blueLegacyApp.webDBSelect'))

    if opcion == "tablas":
        #return redirect(url_for('show_type', sensor="s1"))
        return redirect(url_for('blueLegacyApp.webTabla'))
    
    if opcion == "umbral":
        #Evitar cadena vacia
        if umbraltxt == "":
            umbraltxt = "error"
        return redirect(url_for('blueLegacyApp.webUmbral', umb = umbraltxt))

    if opcion == "media":
        return redirect(url_for('blueLegacyApp.webMedia'))

    if opcion == "grafoBee":
        return redirect(url_for('blueLegacyApp.webGrafoBee'))

    if opcion == "grafo":
        return redirect(url_for('blueLegacyApp.createGraph'))

    if opcion == "plotly":
        #Obtengo el manejador de la BD a 
        #utilizar según la cookie del usuario.
        DBHandler = getCookieDB(request)
        logging.debug("pltly - DBHANDLER: " + str(DBHandler))
        #return redirect(url_for('plotly'))
        plotlyHandler=plotly_manager.PlotlyHandler()
        plotlyHandler.crearGrafo(DBHandler)
        #Abre la gráfica en una nueva pestaña
        #del navegador, por lo que vuelvo a 
        #cargar el menú principal. No necesito
        #cargar otra paǵina.
        return redirect(url_for('blueLegacyApp.webMain'))

    else:
        return "ERROR: Opción Desconocida"
#ELEGIR DB
@blueLegacyApp.route("/seleccDB")
def webDBSelect():
    return render_template("DBselect.html.old")

@blueLegacyApp.route("/seleccDB", methods=['POST'])
def webDBSelect_post():
    opcion = request.form['chosenDB']
    #opcion=request.args.get('chosenDB','default',type=str)
    #Declaro DBHandler como global para que
    #su valor realmente cambie en todo el programa,
    #no solo dentro de esta funcion.
    #
    #Para permitir realmente la concurrencia de usuarios, en
    #vez de emplear la variable DBHandler, vuyo valor se compartirá
    #entre todos los usuarios conectados, haremos que la base de datos
    #a emplear se almacene en las cookies del usuario, de forma que
    #cada uno tenga su valor.
    #
    #Creo la respuesta a la que asignaré las cookies
    response = make_response(redirect(url_for('blueLegacyApp.webMain')))
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
        logging.warning("DB seleccionada descon.")
    #Una vez seleccionada la base de datos,
    #utilizo la funcion reload() para que 
    #pueble las listas globales con los numeros
    #aleatorios y su fecha de obtencion
    #DBHandler.reload()
    #Guardo la base de datos seleccionada en la cookie
    #del cliente.
    #Utilizare la funcion getCookieDB() para, dada
    #la peticion, obtener la cookie del cliente y
    #de alli la base de datos a emplear
    response.set_cookie('db',opcion)
    #return render_template("DBselect.html")
    return response

#TABLAS
@blueLegacyApp.route("/tablas")
def webTabla():
    #Obtengo el manejador de base de datos
    #de la base de datos que haya elegido 
    #el cliente (especificado en su cookie).
    #Si no tiene ninguna, se empleara MongoDB
    DBHandler = getCookieDB(request)

    return render_template("tablas.html.old",\
    tablaHTML = web_presentation.getTableHTML(DBHandler, False),\
    DBName = getDBName(DBHandler))

@blueLegacyApp.route("/tablas", methods=['POST'])
def webTabla_post():
    return redirect(url_for('blueLegacyApp.webMain'))

#UMBRAL
@blueLegacyApp.route("/umbral/<umb>")
def webUmbral(umb):
    #Obtengo el manejador de la BD a 
    #utilizar según la cookie del usuario.
    DBHandler = getCookieDB(request)
    #Obtengo el umbral
    try:
        trueUmbral = float(umb)
    except ValueError:
        logging.warning("NO SE HA INTRODUCIDO NUMERO COMO UMBRAL!")
        umb = "Debe introducirse un numero. Usando valor por defecto: 50."
        trueUmbral = 50
    
    logging.debug("str: " + umb)
    logging.debug("float: " + str(trueUmbral))
    return render_template("umbral.html.old",\
    umbralHTML = umb,\
    resUmbral = web_presentation.getUmbralHTML(DBHandler, trueUmbral , False),\
    DBName = getDBName(DBHandler))
    #resUmbral = "<div>HOLA</div>")

@blueLegacyApp.route("/umbral", methods=['POST'])
def webUmbral_post():
    return redirect(url_for('blueLegacyApp.webMain'))


#MEDIA
@blueLegacyApp.route("/media")
def webMedia():
    #Obtengo el manejador de la BD a 
    #utilizar según la cookie del usuario.
    DBHandler = getCookieDB(request)

    return render_template("media.html.old",\
    resMedia = web_presentation.getMediaHTML(DBHandler, False),\
    DBName = getDBName(DBHandler))

@blueLegacyApp.route("/media", methods=['POST'])
def webMedia_post():
    return redirect(url_for('blueLegacyApp.webMain'))

#GRAFOS REMOTOS (obtenidos de Beebotte)
@blueLegacyApp.route("/grafoBee")
def webGrafoBee():
    #return "Grafo: PLACEHOLDER"
    return render_template("grafoBee.html.old",\
    resGrafo = web_presentation.getGrafoHTML(False))

@blueLegacyApp.route("/grafoBee", methods=['POST'])
def webGrafoBee_post():
    return redirect(url_for('blueLegacyApp.webMain'))

#GRAFOS LOCALES, los creo con la clase GraphMaker en graph_maker.py
@blueLegacyApp.route("/grafo")
def createGraph():
    #Obtengo el manejador de la BD a 
    #utilizar según la cookie del usuario.
    DBHandler = getCookieDB(request)
    
    #Las urls pueden tener las dos siguientes formas:
    #http://0.0.0.0:5000/grafo
    #http://0.0.0.0:5000/grafo?tipo=line
    #Para obtener el valor del argumento tipo en la segunda
    #url emplearemos la siguiente línea de código.
    tipo = request.args.get('tipo')
    #En caso de que la url recibida sea del primer tipo
    #y no contenga parámetros, el valor de tipo será 'None'
    #logging.debug("argumento URL: " + str(tipo))

    #creo instancia
    gm = graph_maker.GraphMaker()
    
    #return gm.crearGrafo(DBHandler)
    
    return render_template("grafoPygal.html.old",\
    nombreDBSimple=getDBSimpleName(DBHandler),\
    graph_data=gm.crearGrafo(DBHandler, tipo),\
    DBName = getDBName(DBHandler))


#CAMBIAR ESTRUCTURA
@blueLegacyApp.route("/grafo", methods=['POST'])
def createGraph_post():
    #obtener datos del form
    try:
        tipoGrafo = request.form['graphType']
        #tipoGrafo=request.args.get('graphType','default',type=str)
    except:
        #logging.debug("Has pulsado volver al menu principal.")
        #Este código se ejecuta cuando se selecciona volver
        #al menú principal en lugar de seleccionar el tipo
        #de lista. Supongo que esto es debido a que si
        #pulsamos el botón volver al menú principal, se esta utilizando
        #el formulario 'volver', por lo que el formulario 'graphType' no 
        #tiene ningún valor y da error al obtenerlo.

        #Si se ha pulsado el botón 'volver al menú principal', pues
        #redirigimos a la página principal
        return redirect(url_for('blueLegacyApp.webMain'))
    try:
        volver = request.form['volver']
        #volver =request.args.get('volver','default',type=str)
    except:
        #logging.debug("Has pulsado Refresh.")
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
        #    logging.debug("argumento: " + str(arg))
        #
        #   2º -> Otra forma es incluir este argumento como un argumento
        #en la propia url. Dentro de la función podemos leer este argumento
        #de la url de la siguiente forma:
        #@app.route("/grafo")
        #def createGraph():
        #    arg = request.args.get('arg')
        #    logging.debug("argumento URL: " + str(arg))
        #
        #La ventaja de este segundo metodo es que no tenemos que definir urls
        #opcionales para la función como en el caso anterior.
        return redirect(url_for('blueLegacyApp.createGraph', tipo=tipoGrafo))

    #No se debería llegar a este punto, pero por si se llega
    #redirigimos al menú principal.
    return redirect(url_for('blueLegacyApp.webMain'))

