# -*- coding: utf-8 -*-
"""
ESCRIBE EL NUMERO ALEATORIO JUNTO
CON LA FECHA Y HORA DE OBTENCION
EN LA BASE DE DATOS LOCAL DE MYSQL
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
#parsear resultados. Expr regulares.
import re
#importamos el fichero rnd_fetcher.py
#en la carpeta web_fetcher.
#En este fichero se encuentra la clase Rnd_fetcher
#que contiene el metodo get_web_rnd() que nos
#devolverá el número aleatorio obtenido de la web.
import web_fetcher.rnd_fetcher as rndF
#para obtener hora y fecha
import date_handler

#-------------------------------------------------------------------------
#CLASE
class SQLHandler:

    #configuramos Flask. SE LO PASAREMOS AL CONSTRUCTOR
    #app = Flask(__name__)

    def __init__(self, flaskApp = Flask(__name__)):
        self.app = flaskApp
        #lista temporal con todas las entradas de mysql (fecha)
        self.listaGlobalFecha = list()
        #lista temporal con todas las entradas de mysql (numeros)
        self.listaGlobalNumero = list()

    """
    #ruta por defecto para ejecutar flask
    @app.route("/")
    def default_function():
        return "Hello World!"
    """

    #FUNCIONES
    #obtenemos el numero aleatorio
    def getData(self):
        clase = rndF.Rnd_fetcher()
        #numero aleatorio
        rnd = clase.get_web_rnd()
        return rnd

    #establecemos la conexion con la base de datos
    def initDBConn(self):
        #SQL config
        mysql = MySQL()
        self.app.config['MYSQL_DATABASE_USER'] = 'lab'
        self.app.config['MYSQL_DATABASE_PASSWORD'] = 'ubuntu16'
        self.app.config['MYSQL_DATABASE_DB'] = 'myFlaskDB'
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        #SQL INIT
        mysql.init_app(self.app)
        conn = mysql.connect()
        return conn


    #escribe el numero aleatorio en la base de datos
    #junto con la fecha y hora de obtencion.
    #Normalmente se especificara el numero a
    #insertar junto con su fecha.
    #Si no es asi, se generará uno.
    def writeDataDB(self, rnd, fecha, debug = False):
        #obtenemos los datos a escribir
        #numero aleatorio. Lo convertimos a String
        #ya que es necesario para meterlo en la orden SQL
        # de cursor.execute()
        #rnd = str(self.getData())
        #fecha en ms
        #fecha = str(date_handler.getDatetimeMs())
        #FECHA Y RND LOS TOMO COMO PARAMETROS
        #debug:
        if debug:
            print "Num: "+rnd+"\nfecha: "+fecha

        #inciiamos conexion con BD
        conn = self.initDBConn()
        #escribimos datos en la BD
        cursor = conn.cursor()
        cursor.execute("insert into NumberList values (%s, %s)", (rnd, fecha))
        res = cursor.fetchall()
        """
        if debug:
            cursor.execute("select * from NumberList")
            res = cursor.fetchall()
            print "La tabla tras la insercion: "
            print res
        """
        #comprobación de errores
        if len(res) is 0:
            conn.commit()
            if debug:
                print 'Query success!'
        else:
            print 'SQL_rnd.py error: ' + str(res[0])
        
        cursor.close()
        conn.close()

    #Lee los datos existentes en la Base de datos
    #Almaceno los datos obtenidos en las listas globales
    def readDataDB(self, debug = False):
        #inciamos conexion con BD
        conn = self.initDBConn()
        #escribimos datos en la BD
        cursor = conn.cursor()
        cursor.execute("select * from NumberList")
        #En res se encuentran todos los datos de la BD
        #en forma de tuplas
        res = cursor.fetchall()
        if debug:
            print "La tabla de la BD: "
            print res
        cursor.close()
        conn.close()
        #DEBUG. para tenerlo disponible desde la consola
        #self.cadenaGlobal = res
        #en longitud tengo el numero de tuplas
        #que hay en el resultado.
        longitud = len(res)
        #inicializamos las listas globales para
        #que tengan esta longitud
        self.listaGlobalFecha = [None] * longitud
        self.listaGlobalNumero = [None] * longitud
        #sacare la fecha y el numero de cada tupla
        for tupla in xrange(longitud):
            cadena = str(res[tupla])
            self.listaGlobalFecha[tupla] = int(self.parseDate(cadena))
            self.listaGlobalNumero[tupla] = float(self.parseNumber(cadena))
            


    #Dada la cadena que se obtiene como resultado de consultar
    #todos los datos de la base de datos, que se obitnenen en
    #de tupla, obtendremos la FECHA.
    #cada tupla tiene la siguiente estructura:
    #(31.95, 1513246490444L)
    def parseDate(self, cadena):
        searchObj = re.search('\((.*?), (.*?)L\)', cadena)
        fecha = searchObj.group(2)
        return fecha

    #Dada la cadena que se obtiene como resultado de consultar
    #todos los datos de la base de datos, que se obitnenen en
    #de tupla, obtendremos el NUMERO.
    #cada tupla tiene la siguiente estructura:
    #(31.95, 1513246490444L)
    def parseNumber(self, cadena):
        searchObj = re.search('\((.*?), (.*?)L\)', cadena)
        num = searchObj.group(1)
        return num

    #Limpia todos los valores de la tabla de MySQL
    def cleanData(self):
        #inciiamos conexion con BD
        conn = self.initDBConn()
        #obtenenmos cursor para ejecutar queries
        cursor = conn.cursor()
        cursor.execute("delete from NumberList where true")
        cursor.close()
        conn.close()

    #permite al usuario añadir canales y variables a los mismos
    def user_op(self):
        repetir = True
        debug_str = raw_input("Activar Modo Debug?[Y\N]: ")
        if debug_str == "Y" or debug_str == "y":
            debug = True
        else:
            debug = False
        #Bucle principal
        while repetir:
            opcion = raw_input("Operacion:\n1.Leer BD.\n2.Escribir BD.\n3.Ver listas temporales.\n")
            #Añadir canal
            if opcion == "1":
                self.readDataDB(debug)
            #Añadir variable
            elif opcion == "2":
                self.writeDataDB(str(self.getData()),
                                str(date_handler.getDatetimeMs()),
                                debug)
            elif opcion == "3":
                print "Lista fechas: "
                print self.listaGlobalFecha
                print "Lista numeros: "
                print self.listaGlobalNumero
            #opcion no valida
            else:
                print "opcion no valida"

            #continuamos con el bucle
            opcion2 = raw_input("Quiere realizar otra operacion? Y/N: ")
            if(opcion2 != "Y" and opcion2 != "y"):
                repetir = False


#LANZAMOS FLASK
if __name__ == "__main__":
    clase = SQLHandler()
    clase.user_op()
    #app.run(host='0.0.0.0')
