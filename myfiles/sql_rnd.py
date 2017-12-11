# -*- coding: utf-8 -*-
"""
ESCRIBE EL NUMERO ALEATORIO JUNTO
CON LA FECHA Y HORA DE OBTENCION
EN LA BASE DE DATOS DE MYSQL
-> BBDD: myFlaskDB
-> Tabla: NumberList
    -> numero, float(5,2).
    -> hora, time.
    -> fecha, date

COMO SE UTILIZA mysql-flask
TENEMOS QUE IMPORTAR FLASK
"""
#flask
from flask import Flask
#mysql-flask
from flaskext.mysql import MySQL
#hacer el sleep
import time
#importamos el fichero rnd_fetcher.py
#en la carpeta web_fetcher.
#En este fichero se encuentra la clase Rnd_fetcher
#que contiene el metodo get_web_rnd() que nos
#devolverá el número aleatorio obtenido de la web.
import web_fetcher.rnd_fetcher as rndF
#para obtener hora y fecha
import date_handler

#configuramos Flask
app = Flask(__name__)

#ruta por defecto para ejecutar flask
@app.route("/")
def default_function():
    return "Hello World!"

#FUNCIONES
#obtenemos el numero aleatorio
def getData():
    clase = rndF.Rnd_fetcher()
    #numero aleatorio
    rnd = clase.get_web_rnd()
    return rnd

#establecemos la conexion con la base de datos
def initDBConn():
    #SQL config
    mysql = MySQL()
    app.config['MYSQL_DATABASE_USER'] = 'lab'
    app.config['MYSQL_DATABASE_PASSWORD'] = 'ubuntu16'
    app.config['MYSQL_DATABASE_DB'] = 'myFlaskDB'
    app.config['MYSQL_DATABASE_HOST'] = 'localhost'
    #SQL INIT
    mysql.init_app(app)
    conn = mysql.connect()
    return conn

#escribe el numero aleatorio en la base de datos
#junto con la fecha y hora de obtencion
def writeDataDB(debug = True):
    #obtenemos los datos a escribir
    #numero aleatorio. Lo convertimos a String
    #ya que es necesario para meterlo en la orden SQL
    # de cursor.execute()
    rnd = str(getData())
    #fecha
    fecha = date_handler.getDate()
    #hora
    hora = date_handler.getTime()
    #debug:
    if debug:
        print "Num: "+rnd+"\nfecha: "+fecha+"\nhora: "+hora

    #inciiamos conexion con BD
    conn = initDBConn()
    #escribimos datos en la BD
    cursor = conn.cursor()
    cursor.execute("insert into NumberList values (%s, %s, %s)", (rnd, hora, fecha))
    res = cursor.fetchall()
    if debug:
        cursor.execute("select * from NumberList")
        print "La tabla tras la insercion: "
        print res
    #comprobación de errores
    if len(res) is 0:
        conn.commit()
        print 'Query success!'
    else:
        print 'error: ' + str(res[0])
    
    cursor.close()
    conn.close()


writeDataDB()

#LANZAMOS FLASK
if __name__ == "__main__":
    app.run(host='0.0.0.0')
