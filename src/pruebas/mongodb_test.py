import pymongo
import random

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

#insertar numero y ~fecha aleatoria
#coll == db.numeros
rand = random.randint(0,100)
fecha = random.randint(200000,299999)
result = coll.insert_one({"num":rand,"tiempo":fecha})

#alamceno en cursor el resultado de obtener todos los 
#documentos (~filas,entradas) en la coleciion 'system.users'.
cursor = coll.find()

#Muestro por pantalla el resultado obtenido
for doc in cursor:
    print doc


#Termino conexion
conn.close()
