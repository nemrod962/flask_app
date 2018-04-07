# -*- coding: utf-8 -*-
"""
Clase con la implementación básica
para comunicarse con MongoDB
"""
import pymongo
import random
#Para errores de conexion con MongoDB
from pymongo.errors import ConnectionFailure

class MongoBasic:

    #Recibe como argumento la coleccion de la que se obtendrán los documentos
    def __init__(self, coleccion="test", limite=1024, debug=False):
        #Inicializo conexion y obtengo el cliente con el que se
        #realizaran las diferentes operaciones.
        #Este atributo contendrá la instancia del cursor
        #devuelto por pymongo.MongoClient(). Simboliza la
        #conexion con la base de datos de MongoDB
        self.con=None
        #Este cliente será un atributo de la instancia de la clase
        #Con el cliente realizamos las consultas.
        #El cliente es en realidad el cursor de la variable
        #anterior pero conectado a una base de datos específica
        #que será con la que trabaje el programa
        self.client=None
        #Atributo que indicará si hay conexión con la base de datos
        #En caso de no haber conexión, no se realizarán las operaciones.
        self.hayConexion=None
        #Coleccion
        self.coleccion=coleccion
        #Limite de documentos maximos devueltos por consulta
        self.limite=limite
        #debug
        self.__debug=debug
        #Damos valor al cliente y la conexion
        self.initConn()
        #...
        #Comprobamos valores
        #print self.con
        #print self.client
        #...
    """
      ____                            _   _             
     / ___|___  _ __  _ __   ___  ___| |_(_) ___  _ __  
    | |   / _ \| '_ \| '_ \ / _ \/ __| __| |/ _ \| '_ \ 
    | |__| (_) | | | | | | |  __/ (__| |_| | (_) | | | |
     \____\___/|_| |_|_| |_|\___|\___|\__|_|\___/|_| |_|
    """

    #Inicializo la conexion
    def initConn(self):
        #Obtengo credenciales del fichero.
        #Un dato por línea
        try:
            mongo_key_file=open("credentials/mongo_credentials", "r")
            host=mongo_key_file.readline().rstrip()
            port=mongo_key_file.readline().rstrip()
            user=mongo_key_file.readline().rstrip()
            passw=mongo_key_file.readline().rstrip()
            db=mongo_key_file.readline().rstrip()

        #Si fallo en abrir fichero, utilizo credenciales por defecto
        except IOError:
            if self.__debug:
                print "Fallo al abrir archivo credenciales!"
            host='localhost'
            port='8080'
            user='pablo'
            passw='123456'
            db='mydb'

        #Creo cliente para la conexion con la base de datos especificada
        con = pymongo.MongoClient('mongodb://'+user+':'+passw+'@'+host+':'+port+'/')
        #Asigno a la variable client la conexion con la base de datos
        #de mongoDB especificada en el archivo de credenciales.
        #Será más cómodo de utilizar que la variable 'con'.
        client = con[db]

        #Asigno a los atributos de la clase las conexiones que acabamos
        #de crear.
        self.con = con
        self.client = client
        
        #La validez de estas conexiones la indicará la conectivida,
        #indicada a su vez por el atributo de la clase hayConexion

        #Compruebo conectividad con MongoDB
        try:
            # The ismaster command is cheap and does not require auth.
            con.admin.command('ismaster')
            #Si no salta la excepcion con la orden anterior
            #significara que hay conexion
            self.hayConexion=True
        except ConnectionFailure:
            print("MongoDB server not available")
            #Si ha saltado la exception no hay conexion
            self.hayConexion=False


    #Comprobar Conexion. Devuelve True si hay conexion, False si no la hay.
    def checkConn(self):
        try:
            # The ismaster command is cheap and does not require auth.
            self.con.admin.command('ismaster')
            #Si no salta la excepcion con la orden anterior
            #significara que hay conexion
            self.hayConexion=True
        except ConnectionFailure:
            print("MongoDB server not available")
            #Si ha saltado la exception no hay conexion
            self.hayConexion=False
        finally:
            return self.hayConexion
    
    #Termino la conexion
    def endConn(self):
        if self.__debug:
            print "Cerrando conexion MongoDB."
        #try:
            self.con.close()
        #Si con == None    
        #except AttributeError as e:
        #    print "No habia conexion: "+ str(e)

    #Funciones Misceláneas

    #Obtener colección actual
    def getColeccion(self):
        return self.coleccion
    
    #Cambiar coleccion 
    def setColeccion(self, coleccion):
        self.coleccion=coleccion

    
    """
     ____                _ 
     |  _ \ ___  __ _  __| |
     | |_) / _ \/ _` |/ _` |
     |  _ <  __/ (_| | (_| |
     |_| \_\___|\__,_|\__,_|
                            
    """

    #Obtener documentos.
    #Si no se aportan argumentos, devolverá todos los documentos en la coleccion
    #con todos sus campos.
    #Si no hay conexion, retorna None
    def leer(self, campo=None):
        #Si no hay conexión, no ejecutamos la función
        if self.checkConn():
            #Si no se especifica campo, o el campo introducido no es string
            #Si campo==None, entonces isinstance(campo, str) = False
            if not isinstance(campo, str):
                if self.__debug and campo!=None:
                    print "Nombre de campo introducido no válido!"
                #Obtengo cursor a la collecion
                col=self.client[self.coleccion]
                #Realizo la consulta a la coleecion
                res=col.find().limit(self.limite)
                #Muestro los resultados obtenidos
                if self.__debug:
                    i=0
                    print "Leyendo de MongoDB:"
                    for doc in res:
                        print str(i)+": " + str(doc)
                        i=i+1
            else:
                #Si se ha especificado un campo, solo devuelvo ese campo
                #Obtengo cursor a la collecion
                col=self.client[self.coleccion]
                #Realizo la consulta a la coleecion
                res=col.find({},{"_id":0,campo:1}).limit(self.limite)
                if self.__debug:
                    i=0
                    print "Leyendo de MongoDB:"
                    for doc in res:
                        print str(i)+": " + str(doc)
                        try:
                            print str(i)+": " + str(doc[campo])
                        except:
                            print "No se pudo leer campo: " + str(campo)
                        i=i+1

            #Antes de salir
            #retornamos el puntero al inicio del cursor,
            #de forma que si queremos iterar a través de
            #él con un for para realizar cualquier operación
            #sobre los documentos que contiene podamos hacerlo
            res.rewind()
            return res

        #Si no hay conexion, retorno None
        return None

    #Obtener documentos ordenados por campo.
    #Si no se aportan argumentos, devolverá todos los documentos en la coleccion
    #con todos sus campos.
    #El orden por defecto es ascendente, de menor a mayor.
    #Si no hay conexion, retorno None
    def leerOrden(self, campo, ordenAsc=True):
        #Si no hay conexión, no ejecuto la función
        if self.checkConn():
            #Defino el orden
            if ordenAsc:
                orden=pymongo.ASCENDING
            else:
                orden=pymongo.DESCENDING
            #Si el campo introducido es valido, ordeno por ese campo.
            #Si no devuelvo todo, ignorando el campo
            if isinstance(campo, str):
                #Obtengo cursor a la collecion
                col=self.client[self.coleccion]
                #Realizo la consulta a la coleecion
                res=col.find().sort(campo,orden).limit(self.limite)
                if self.__debug:
                    i=0
                    print "Leyendo (ordenadamente) de MongoDB:"
                    for doc in res:
                        print str(i)+": " + str(doc)
                        i=i+1
            else:
                if self.__debug:
                    print "Nombre de campo introducido no válido!"
                res = self.leer()
            
            #Retornamos el puntero al inincio del cursor
            res.rewind()
            return res
        #Si no hay conexion retorno None
        return None

    #Obtener documentos que cumplan cierta condición.
    #La condición debe ser de tipo dict.
    #e.g cond -> {"num": {'$gt': 90} }
    #El resultado podrá ordenarse opcionalmente según un campo
    def leerCondicion(self, condicion, campo, ordenAsc=True):
        #Si no hay conexión, no ejecuto la función
        if self.checkConn():
            #Defino el orden
            if ordenAsc:
                orden=pymongo.ASCENDING
            else:
                orden=pymongo.DESCENDING

            #Comprobar tipo condicion
            if isinstance(condicion, dict):
                #Obtengo cursor de la coleccion
                col=self.client[self.coleccion]
                #Compruebo si el parametro campo es string
                if isinstance(campo, str):
                    #Realizo la consulta ordenando por campo
                    res=col.find(condicion).sort(campo,orden).limit(self.limite)
                else:
                    if self.__debug:
                        print "Sin ordenar, nombre de campo no valido."
                    #Realizo consulta sin ordenar
                    res=col.find(condicion).limit(self.limite)
                
                if self.__debug:
                    print "leerCondicion - Resultado: "
                    if res.count == 0:
                        print "ATENCION: resultado de la consulta vacio."
                        print "Es probable que la condición no sea valida."
                    for doc in res:
                        print doc
                    res.rewind()
                #Devuelvo el resultado de la consulta
                return res
                

            #La condicion no es valida pues no es de tipo dict.
            #Devuelvo -1 para indicar error
            else:
                if self.__debug:
                    print "leerCondicion(): Condición no válida: "+str(condicion)
                return -1

        #Si no hay conexion retorno None
        return None


    """
    __        __    _ _       
    \ \      / / __(_) |_ ___ 
     \ \ /\ / / '__| | __/ _ \
      \ V  V /| |  | | ||  __/
       \_/\_/ |_|  |_|\__\___|

    """
    #El argumento recibido debe ser del tipo 'dict'.
    #Debe tener un formato similar al siguiente:
    #e.g. {"dato1":valor1,"dato2":valor2,...,"dato_n":valor_n}
    #Devuelve 0 si se escribió satisfactoriamente, 1 en caso contrario
    #Devuelve -1 si no hay conexion con MongoDB
    def escribir(self, datos):
        #Si no hay conexión, no ejecutamos la función
        if self.checkConn():
            #Me aseguro del tipo del parametro recibido
            #También me aseguro de que el diccionario no está vacío
            if isinstance(datos, dict) and any(datos):
                #Obtengo cursor a la collecion
                col=self.client[self.coleccion]
                #Realizo la consulta a la coleecion
                try:
                    #res0 contendrá el _id que le ha asignado Mongo a los datos.
                    res0=col.insert(datos)
                    #print res0
                    res=0
                except Exception as e:
                    print "MongoBasic.escribir() - ERROR: " + str(e)
                    res0=1
                
            else:
                if self.__debug:
                    if not isinstance(datos, dict):
                        print "Los datos proporcionados no son de tipo dict!"
                    elif not any(datos):
                        print "Los datos proporcionados estan vacios!"
                res=1

            return res
        #Si no hay conexión, retorno -1
        else:
            return -1
        

    """
      ____       _      _       
     |  _ \  ___| | ___| |_ ___ 
     | | | |/ _ \ |/ _ \ __/ _ \
     | |_| |  __/ |  __/ ||  __/
     |____/ \___|_|\___|\__\___|
                                
    """
    #Borra todos los documentos que cumplan conla condición dada.
    #La condicion debe introducirse como un diccionario.
    #e.g. {"num", {"$gt":30}}
    #para borrar TODO -> {}
    #para borrar campo vacio -> {"num": {"$exists": False}}
    #para borrar todos documentos con campo "var" 
    # -> {"var":{"$regex": ".*"}}
    #Devuelve el número de documentos borrados.
    #Devuelve -2 en caso de error.
    #Debuelve -1 si no hay conexión con MongoDB.
    def borrar(self, condicion):
        #Si no hay conexión, no ejecutamos la función
        if self.checkConn():
            if isinstance(condicion, dict):
                #Obtengo cursor a la collecion
                col=self.client[self.coleccion]
                error=False
                try:
                    #Realizo la consulta a la coleecion
                    res0=col.delete_many(condicion)
                    res=res0.deleted_count
                except Exception as e:
                    print "MongoBasic.borrar() - ERROR: " + str(e)
                    res=-2
                    error=True
                
                #Debug
                if self.__debug and not error :
                    print "Se han borrado " +  str(res0.deleted_count) + " documentos."
            else:
                if self.__debug:
                    if not isinstance(condicion, dict):
                        print "Los datos proporcionados no son de tipo dict!"
                res=-2

            return res
        #Si no hay conexión devuelvo -1
        else:
            return -1


    """
      _   _           _       _       
     | | | |_ __   __| | __ _| |_ ___ 
     | | | | '_ \ / _` |/ _` | __/ _ \
     | |_| | |_) | (_| | (_| | ||  __/
      \___/| .__/ \__,_|\__,_|\__\___|
           |_|                        
    """
    #Los documentos que cumplan con condicion se 
    #les realizará la signación.
    #Tanto la condición como la asignación deben 
    #ser de tipo dict.
    #e.g cond -> {"num": {'$gt': 90} }
    #e.g asig -> {"tiempo": 0}
    #Devuelve el número de documentos borrados.
    #Devuelve -2 en caso de error.
    #Debuelve -1 si no hay conexión con MongoDB.
    def actualizar(self, condicion, asignacion):
        #Si no hay conexión, no ejecutamos la función
        if self.checkConn():
            if isinstance(condicion, dict) and isinstance(asignacion, dict):
                #Obtengo cursor a la collecion
                col=self.client[self.coleccion]
                error = False
                try:
                    #Realizo la consulta a la coleecion
                    res0=col.update_many(condicion, {"$set": asignacion})
                    res=res0.modified_count
                except Exception as e:
                    print "MongoBasic.actualizar() - ERROR: " + str(e)
                    error=True
                    res = -2
                #Debug
                if self.__debug and not error:
                    print "Cumplen la condición " +  str(res0.matched_count) + " documentos."
                    print "Se han modificado " +  str(res0.modified_count) + " documentos."
            else:
                if self.__debug:
                    if not isinstance(condicion, dict):
                        print "Los datos de condicion proporcionados no son de tipo dict!"
                    if not isinstance(asignacion, dict):
                        print "Lo datos de asignacion proporcionados no son de tipo dict!"
                res=-2

            return res
        #Si no hay conexión, retorno -1
        else:
            return -1

#Al ejecutar como main
if __name__ == "__main__":
    m = MongoBasic("test",1024,True)
    #res3=m.leerOrden("tiempo",True)

    #escribir
    r=random.randint(0,100)
    t=random.randint(2000000,2999999)
    m.escribir({"var" : "descr1" , "num" : r , "tiempo" : t})
    
    
    #borrar
    dato={"var":{"$regex": ".*"}}
    res3 = m.borrar(dato)
    print "Borrados: " + str(res3)
    
    """
    #actualizar
    con={"num": {"$gt":50}}
    asig={"tiempo": 777}
    res1=m.actualizar(con, asig)
    print "Actualizados: " + str(res1)
    """
    #leer
    res2=m.leer()
    
    #dato="num"
    #print "res1"
    #for doc in res1:
    #    print doc[dato]
    #print res1
    #print "res2"
    #for doc in res2:
    #    print doc
    #print "res3"
    #print res3
    m.endConn()

