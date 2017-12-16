# -*- coding: UTF-8 -*-
"""
EJEMPLO INICIAL DE FLASK
"""
#proceso para subir los datos a las BBDD
import rnd_uploader
#funcionalidad de la web con los datos
import web_functions

from flask import Flask 
app = Flask(__name__) 

@app.route("/") 

def hello():
   return "Hello World!"

if __name__ == "__main__":

   #Iniciar y lanzar proceso de carga de datos en las BBDD
   #LOS MANEJADORES DE LAS DBs SE INICIALIZAN EN SU CONSTRUCTOR
   uploader = rnd_uploader.RndUploader(app, 120, True)    

   #prueba
   r1 = data_functions.umbral(uploader.getSQLHandler(), 50, True) 
   r2 = data_functions.umbral(uploader.getBeeHandler(), 50, True) 
   r3 = data_functions.umbral(None, 50) 
   media1 = data_functions.media(uploader.getSQLHandler(), True)
   media2 = data_functions.media(uploader.getBeeHandler(), True)
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
    
   #app.run(host='0.0.0.0')
    
   #señal de finalizar al proceso
   #uploader.enable = False

   uploader.finalizar()

   print "FIN"
