import pymongo
import random
#import json

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

"""
#insertar numero y ~fecha aleatoria
#coll == db.numeros
rand = random.randint(0,100)
fecha = random.randint(200000,299999)
#result = coll.insert({"num":rand,"tiempo":fecha})
result = coll.insert({"tiempo":fecha,"num":rand})
"""

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
