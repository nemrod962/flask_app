# -*- coding: UTF-8 -*-
"""
EJEMPLO INICIAL DE FLASK
"""
#FLASK
from flask import Flask, render_template, url_for, redirect, request
#proceso para subir los datos a las BBDD
import rnd_uploader
#funcionalidad de la web con los datos
import web_functions
import web_presentation
#Manejo Bases de Datos
import sql_rnd
import beebotte_rnd

#Creo instancia de Flask
app = Flask(__name__) 

#VAR GLOBAL
#Manejo de BBDD
SQLHandler = sql_rnd.SQLHandler(app)
BeeHandler = beebotte_rnd.BeeHandler()

#PAGINA INICIAL
#Mostramos la pagina inicial
@app.route("/") 
def webMain():
    return render_template("index.html")

#Procesamos la opción elegida en la pagina inicial
@app.route("/", methods=['POST'])
def webMain_post():
    opcion = request.form['option']
    
    #Dependiendo de la direccion seleccionada en
    #la pantalla inicial redirigiremos a una dirección 
    #o a otra.

    if opcion == "tablas":
        #return redirect(url_for('show_type', sensor="s1"))
        return redirect(url_for('webTabla'))

    if opcion == "umbral":
        return redirect(url_for('webUmbral'))

    if opcion == "media":
        return redirect(url_for('webMedia'))

    if opcion == "grafo":
        return redirect(url_for('webGrafo'))

    else:
        return "ERROR: Opción Desconocida"

#TABLAS
@app.route("/tablas")
def webTabla():
    #return "Tablas: PLACEHOLDER"
    return render_template("tablas.html",\
    tablaHTML = web_presentation.getTableHTML(SQLHandler, True))

@app.route("/tablas", methods=['POST'])
def webTabla_post():
    return redirect(url_for('webMain'))

#UMBRAL
@app.route("/umbral")
def webUmbral():
    #return "Umbral: PLACEHOLDER"
    return render_template("umbral.html",\
    resUmbral = web_presentation.getUmbralHTML(BeeHandler, 50, True))
    #resUmbral = "<div>HOLA</div>")

@app.route("/umbral", methods=['POST'])
def webUmbral_post():
    return redirect(url_for('webMain'))

#MEDIA
@app.route("/media")
def webMedia():
    #return "Media: PLACEHOLDER"
    return render_template("media.html",\
    resMedia = web_presentation.getMediaHTML(BeeHandler, True))

@app.route("/media", methods=['POST'])
def webMedia_post():
    return redirect(url_for('webMain'))

#GRAFOS
@app.route("/grafo")
def webGrafo():
    return "Grafo: PLACEHOLDER"

@app.route("/grafo", methods=['POST'])
def webGrafo_post():
    return redirect(url_for('webMain'))

if __name__ == "__main__":

   #Iniciar y lanzar proceso de carga de datos en las BBDD
   #LOS MANEJADORES DE LAS DBs SE INICIALIZAN EN SU CONSTRUCTOR
   uploader = rnd_uploader.RndUploader(app, SQLHandler, BeeHandler, 120, True) 
   #prueba
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
    
   app.run(host='0.0.0.0')
    
   #señal de finalizar al proceso
   #uploader.enable = False

   uploader.finalizar()

   print "FIN"
