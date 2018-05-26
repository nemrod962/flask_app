# -*- coding: UTF-8 -*-

#Dado como argumento un manejador de BD nos dice si 
#es de MySQL o Beebotte. Se empleará para obtener el 
#tipo de base de datos que se esta utilizando dado
#su manejador
def getDBName(DBHandler):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler":
        return "MySQL (local)"
    elif DBHandler.__class__.__name__ == "BeeHandler" :
        return "Beebotte (online)"
    elif DBHandler.__class__.__name__ == "MongoHandler" :
        return "MongoDB (local)"
    else:
        return "Descon."

def getDBSimpleName(DBHandler):
    #Usamos MySQL o Beebotte
    if DBHandler.__class__.__name__ == "SQLHandler":
        return "mysql"
    elif DBHandler.__class__.__name__ == "BeeHandler" :
        return "beebotte"
    elif DBHandler.__class__.__name__ == "MongoHandler" :
        return "mongodb"
    else:
        return "desconocido"

