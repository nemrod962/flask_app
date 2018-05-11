#!/bin/bash
if [ -z "$1" ]
then
    CNAME="flask-mongo"
else
    CNAME=$1
fi

if [ -z "$2" ]
then
    NPORT=8080
else
    NPORT=$2
fi
echo "container name: $CNAME"
echo "mappped to port: $NPORT"
# get mongo image
sudo docker pull mongo
# create mongo container called as the variable CONTAINERNAME
sudo docker run --name $CNAME -p $NPORT:27017 -d mongo --auth
# add initial admin user. Default is 'root' as user and password
# to change them. Modify the mongoAddAdminConfig file
sudo docker exec -i $CNAME mongo admin < mongoAddAdminConfig


#-------------------------
#Para acceder a la base de datos en línea de comandos emplear la siguiente orden
#docker run -it --rm --link $CNAME:mongo mongo mongo -u root -p root --authenticationDatabase admin $CNAME/mydb

#Para crear un usuario admin:
#db.createUser(
#  {
#    user: "root",
#    pwd: "root",
#    roles: [ { role: "root", db: "admin" } ]
#  }
#);
