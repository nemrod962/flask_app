# -*- coding: utf-8 -*-
"""
LEGACY
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
#logging
import logging
from log_handler import setup_log


#-------------------------------------------------------------------------
#CLASE
class SQLHandler:

    #configuramos Flask. SE LO PASAREMOS AL CONSTRUCTOR
    #app = Flask(__name__)

    def __init__(self, flaskApp = Flask(__name__)):
        
        #Instancia de Flask a utilizar para configurar la conexion
        self.app = flaskApp
        #lista temporal con todas las entradas de mysql (fecha)
        self.listaGlobalFecha = list()
        #lista temporal con todas las entradas de mysql (numeros)
        self.listaGlobalNumero = list()
        """
        Modoa prueba de fallos. En caso de que no se pueda conectar
        a una instancia local de mysql, se activará este modo, de forma
        que esta clase no realizará ninguna función pero evitara el 
        crasheo de la aplicación.
        En un principio stará desactivado, pero si fallamos al conectar
        a la base da datos en la funcion initDBConn(), lo activamos.
        """
        self.modoPruebaFallos=False

        #-----
        #Lo ejecutamos una vez de forma que se 
        #active el modo a prueba de fallos si no hay
        #una base de datos mysql en el equipo
        self.initDBConn()


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
        #En vez de establecer credenciales a mano,
        #las leo de un fichero
        """
        self.app.config['MYSQL_DATABASE_USER'] = 'lab'
        self.app.config['MYSQL_DATABASE_PASSWORD'] = 'ubuntu16'
        self.app.config['MYSQL_DATABASE_DB'] = 'myFlaskDB'
        self.app.config['MYSQL_DATABASE_HOST'] = 'localhost'
        """
        #Abro fichero. 
        try:
            import json
            sql_key_file=open("credentials/sql_credentials.json", "r")
            #Debo leer los datos del fichero json
            data = json.load(sql_key_file)
            self.app.config['MYSQL_DATABASE_USER']=data['user']
            self.app.config['MYSQL_DATABASE_PASSWORD']=data['pass']
            self.app.config['MYSQL_DATABASE_DB']=data['database']
            self.app.config['MYSQL_DATABASE_HOST']=data['host']
            #cierro fichero
            sql_key_file.close()
        except IOError as e:
            logging.warning("MySQL Handler: " + str(e))
        #SQL INIT
       	mysql.init_app(self.app)
        try:
            conn = mysql.connect()
        except:
            logging.warning("NO SE PUDO CONECTAR A MYSQL.")
            #Inicializamos conn
            conn = None
            #Activar modo a preba de fallos
            self.modoPruebaFallos=True
            #logging.debug(self.modoPruebaFallos)
        return conn


    #escribe el numero aleatorio en la base de datos
    #junto con la fecha y hora de obtencion.
    #Normalmente se especificara el numero a
    #insertar junto con su fecha.
    #Si no es asi, se generará uno.
    #DEVULVE 0 SI BIEN. SI NO 1.
    def writeDataDB(self, numRnd, fecha, debug = False):
        
        #Solo ejecuto realmente esta funcion si he
        #logrado realmente conectarme a la base de datos,
        #es decir, si el modo a prueba de fallos no esta
        #activado, es decir, si tengo conexion con la BD.
        if debug:
            logging.debug("writeDataDb - MODO PRUEBA FALLOS: " + str(self.modoPruebaFallos))
        if self.modoPruebaFallos==False:
            #obtenemos los datos a escribir
            #numero aleatorio. Lo convertimos a String
            #ya que es necesario para meterlo en la orden SQL
            # de cursor.execute()
            #PASO DE INT A STRING
            #es necesario tenerlo en string pues la orden SQL
            #es una cadena, y como vamos a poner el numero 
            #en esa cadena deberá ser del tipo string
            rnd = str(numRnd)
            #fecha en ms
            #fecha = str(date_handler.getDatetimeMs())
            #FECHA Y RND LOS TOMO COMO PARAMETROS
            #debug:
            if debug:
                logging.debug("Num: "+rnd+"\nfecha: "+fecha)

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
                logging.debug("La tabla tras la insercion: ")
                logging.debug(res)
            """
            #comprobación de errores
            if len(res) is 0:
                conn.commit()
                if debug:
                    logging.debug('Query success!')
                #OK
                result =  0
            else:
                logging.debug('SQL_rnd.py error: ' + str(res[0]))
                #NO OK
                result = 1
            cursor.close()
            conn.close()
            return result
        else:
            return 1



    #ACTUALIZO LAS LISTAS LOCALES CON LOS DATOS DE LA BD
    #Lee los datos existentes en la Base de datos
    #Almaceno los datos obtenidos en las listas globales
    def readDataDB(self, debug = False):

        #Solo ejecuto realmente esta funcion si he
        #logrado realmente conectarme a la base de datos,
        #es decir, si el modo a prueba de fallos no esta
        #activado.
        if debug:
            logging.debug("readDataDB - MODO PRUEBA FALLOS: " + str(self.modoPruebaFallos))
        if self.modoPruebaFallos==False:

            #inciamos conexion con BD
            conn = self.initDBConn()
            #escribimos datos en la BD
            cursor = conn.cursor()
            cursor.execute("select * from NumberList")
            #En res se encuentran todos los datos de la BD
            #en forma de tuplas
            res = cursor.fetchall()
            if debug:
                logging.debug("La tabla de la BD: ")
                logging.debug(res)
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


        #Solo ejecuto realmente esta funcion si he
        #logrado realmente conectarme a la base de datos,
        #es decir, si el modo a prueba de fallos no esta
        #activado
        if debug:
            logging.debug("cleanData - MODO PRUEBA FALLOS: " + str(self.modoPruebaFallos))
        if self.modoPruebaFallos==False:

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
                logging.debug("Lista fechas: ")
                logging.debug(self.listaGlobalFecha)
                logging.debug("Lista numeros: ")
                logging.debug(self.listaGlobalNumero)
            #opcion no valida
            else:
                logging.debug("opcion no valida")

            #continuamos con el bucle
            opcion2 = raw_input("Quiere realizar otra operacion? Y/N: ")
            if(opcion2 != "Y" and opcion2 != "y"):
                repetir = False

    #INTERFAZ PARA CARGAR EN LAS LISTAS GLOBALES
    #LOS DATOS DE LAS BASES DE DATOS.
    #Este metodo se llamará igual tanto en el
    #manejador de SQL como de Beebotte.
    def reload(self):
        self.readDataDB()

#LANZAMOS FLASK
if __name__ == "__main__":
    setup_log()
    clase = SQLHandler()
    clase.user_op()
    #app.run(host='0.0.0.0')
