# -*- coding: UTF-8 -*-
"""
EJEMPLO INICIAL DE FLASK
"""
#proceso para subir los datos a las BBDD
import rnd_uploader

from flask import Flask 
app = Flask(__name__) 

@app.route("/") 

def hello():
   return "Hello World!"

if __name__ == "__main__":
   
   #Iniciar y lanzar proceso de carga de datos en las BBDD
   uploader = rnd_uploader.RndUploader(app, 10, True)

   app.run(host='0.0.0.0')
    
   #señal de finalizar al proceso
   #uploader.enable = False

   uploader.finalizar()

   print "FIN"
