
#Descargo docker de MongoDB
docker pull mongo

#SETUP
#Crear docker my-mongo.
#Accederé a Mongo a través del puerto 8080.
docker run --name my-mongo -p 8080:27017 -d mongo --auth
#Ejecuto mongoDB sin credenciales
docker exec -it my-mongo mongo admin

#Dentro de mongo creo usuario root
db.createUser(
  {
    user: "pablo",
    pwd: "123456",
    roles: [ { role: "root", db: "admin" } ]
  }
);

#Iniciar mongo con las credenciales
#Incicio contenedor en caso de haberlo parado previamente
docker start my-mongo
#Inicio mongo obligando a aportar credenciales
docker run -it --rm --link my-mongo:mongo mongo mongo -u pablo -p 123456 --authenticationDatabase admin my-mongo/mydb

