# -*- coding: utf-8 -*-
"""
Clase con la implementación básica
para comunicarse con MongoDB
"""
import pymongo
import random

class MongoBasic:

    #Recibe como argumento la coleccion de la que se obtendrán los documentos
    def __init__(self, coleccion, limite=1024, debug=False):
        #Inicializo conexion y obtengo el cliente con el que se
        #realizaran las diferentes operaciones.
        #Este cliente será un atributo de la instancia de la clase
        #Con el cliente realizamos las consultas
        self.client=None
        #Este atributo solo se empleara para cerrar la conexion
        self.con=None
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
        print self.con
        print self.client
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
        except:
            if self.__debug:
                print "Fallo al abrir archivo credenciales!"
            host='localhost'
            port='8080'
            user='pablo'
            passw='123456'
            db='mydb'

        #Creo cliente para la conexion con la base de datos especificada
        con = pymongo.MongoClient('mongodb://'+user+':'+passw+'@'+host+':'+port+'/')
        client = con[db]
        
        #Asigno valores a los atributos de la clase
        self.con = con
        self.client = client
    
    #Termino la conexion
    def endConn(self):
        if self.__debug:
            print "Cerrando conexion MongoDB."
        self.con.close()
    
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
    def leer(self, campo=None):
        #Si no se especifica campo, o el campo introducido no es string
        if campo==None or not isinstance(campo, str):
            if self.__debug and not isinstance(campo, str):
                print "Nombre de campo introducido no válido!"
            #Obtengo cursor a la collecion
            col=self.client[self.coleccion]
            #Realizo la consulta a la coleecion
            res=col.find().limit(self.limite)
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

        return res

    #Obtener documentos ordenados por campo.
    #Si no se aportan argumentos, devolverá todos los documentos en la coleccion
    #con todos sus campos.
    #El orden por defecto es ascendente, de menor a mayor.
    def leerOrden(self, campo, ordenAsc=True):
            #Defino el orden
            if ordenAsc:
                orden=1
            else:
                orden=0
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

            return res

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
    def escribir(self, datos):
        #Me aseguro del tipo del parametro recibido
        #También me aseguro de que el diccionario no está vacío
        if isinstance(datos, dict) and any(datos):
            #Obtengo cursor a la collecion
            col=self.client[self.coleccion]
            #Realizo la consulta a la coleecion
            try:
                res0=col.insert(datos)
            except Exception as e:
                print "MongoBasic.escribir() - ERROR: " + str(e)
                res0=-1
            print res0
            res=0
            
        else:
            if self.__debug:
                if not isinstance(datos, dict):
                    print "Los datos proporcionados no son de tipo dict!"
                elif not any(datos):
                    print "Los datos proporcionados estan vacios!"
            res=1

        return res
        

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
    def borrar(self, condicion):
        if isinstance(condicion, dict):
            #Obtengo cursor a la collecion
            col=self.client[self.coleccion]
            #Realizo la consulta a la coleecion
            error=False
            try:
                res0=col.delete_many(condicion)
            except Exception as e:
                print "MongoBasic.borrar() - ERROR: " + str(e)
                error=True
            res=0
            if self.__debug and not error :
                print "Se han borrado " +  str(res0.deleted_count) + " documentos."
        else:
            if self.__debug:
                if not isinstance(condicion, dict):
                    print "Los datos proporcionados no son de tipo dict!"
            res=1

        return res


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
    def actualizar(self, condicion, asignacion):
        if isinstance(condicion, dict) and isinstance(asignacion, dict):
            #Obtengo cursor a la collecion
            col=self.client[self.coleccion]
            #Realizo la consulta a la coleecion
            error = False
            try:
                res0=col.update_many(condicion, {"$set": asignacion})
            except Exception as e:
                print "MongoBasic.actualizar() - ERROR: " + str(e)
                error=True
            res=0
            if self.__debug and not error:
                print "Cumplen la condición " +  str(res0.matched_count) + " documentos."
                print "Se han modificado " +  str(res0.modified_count) + " documentos."
        else:
            if self.__debug:
                if not isinstance(condicion, dict):
                    print "Los datos de condicion proporcionados no son de tipo dict!"
                if not isinstance(asignacion, dict):
                    print "Lo datos de asignacion proporcionados no son de tipo dict!"
            res=1

        return res

#Al ejecutar como main
if __name__ == "__main__":
    m = MongoBasic("numeros",1024,True)
    #res3=m.leerOrden("tiempo",True)
    dato={"var":{"$regex": ".*"}}
    res3 = m.borrar(dato)
    con={"num": {"$gt":50}}
    asig={"tiempo": 777}
    res1=m.actualizar(con, asig)
    res2=m.leer()
    
    dato="num"
    print "res1"
    #for doc in res1:
    #    print doc[dato]
    print res1
    print "res2"
    for doc in res2:
        print doc
    print "res3"
    print res3
    m.endConn()

"""
#----------------
#Conectarse con MongoDB en localhost puerto 8080
#con el usuario pablo y la contrasenna 123456
host='localhost'
port='8080'
user='pablo'
passw='123456'
conn=pymongo.MongoClient('mongodb://'+user+':'+passw+'@'+host+':'+port+'/')

#Almaceno en db la bd 'admin'
#db=conn['admin']
db=conn['mydb']

#alamceno en coll la coleccion (~tabla) 'system.users'
#coll=db['system.users']
coll=db['numeros']

#
#insertar numero y ~fecha aleatoria
#coll == db.numeros
rand = random.randint(0,100)
fecha = random.randint(200000,299999)
#result = coll.insert({"num":rand,"tiempo":fecha})
result = coll.insert({"tiempo":fecha,"num":rand})
#

#cambio el tiempo de los  numeros mayores de 90 a 0.
print "UPDATE!"
res = db.numeros.update_many({"num": {'$gt': 90} }, {'$set': {"tiempo": 0} })
print "Coincidencias: " + str(res.matched_count)
print "Modificiaciones: " + str(res.modified_count)

#borrar Una entrada que tenga el num 100.
#Para borrar todas usar delete_many
res = db.numeros.delete_one({"num": 100})
print "BORRADOS: " + str(res.deleted_count)

#almaceno en cursor el resultado de obtener todos los 
#documentos (~filas,entradas) en la coleciion 'system.users'.
#Con .limit() podemos limitar el numero de documentos devueltos
#cursor = coll.find().sort("num",1)
cursor = coll.find().limit(5).sort("num",1)
#Obtengo solo los numeros mas grades de 50.
#Ordeno los resultados enorden ascendente.
#cursor = coll.find({"num": {"$gt":50}}, {"num": 1, "_id": 0}).sort("num", 1)



listaNum=list()
#Muestro por pantalla el resultado obtenido
#Cada doc es de typo 'dict'
for doc in cursor:
    print doc
    print type(doc)
    print "Entrada:"
    print str(doc['num'])
    #Agrego
    listaNum.append(doc['num'])
    print "Lista:" + str(listaNum)


#Termino conexion
conn.close()
"""
