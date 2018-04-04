# -*- coding: utf-8 -*-
"""
Clase encargada de guardar y consultar los usuarios
almacenados en MongoDB.

Estructura de los documentos almacenando usuarios en MongoDB
Campos:
    -> username: nombre de usuario
    -> password: hash de la contraseña
    -> session_id: valor que almacenaremos temporalmente como
    id de la sesion (cookie) del usuario. Tendrá un valor por defecto
    que indicara que no hay sesion abierta (-1).
    En lugar de eso, mantendré una variable (diccionario?) durante tiempo
    de ejecucion (similiar a listaGlobalNumero) donde mantendré los paresde
    valores de usuario y el valor de su cookie para la sesión actual
    -> umbral: Si se obtiene un numero aleatorio superior al umbral,se le
    notificara al usuario.

"""
from mongo_base import MongoBasic

class UserManager(MongoBasic):
    
    #Contructor
    def __init__(self, coleccionUsuarios="usuariosFlask", debug=True):
        MongoBasic.__init__(self, coleccionUsuarios, 1024, debug)

        self.campoUsername="username"
        self.campoPassword="password"
        #self.campoSession="session_id"
        self.campoUmbral="umbral"
        #Diccionario que contiene los pares de cookie y usuario correspondiente
        self.listaSesiones=dict()

        #Debug
        self.debug=debug



    #Login.
    #Verifica si el usuario indicado existe.
    #De ser así, devuelve el valor de la cookie para la 
    #sesion actual del usuario.
    #Si el usuario indicado no existe, o la contraseña es
    #incorrecta, devolveremos -1.
    def login(self, userId, userPass):
        condicion={self.campoUsername : userId}
        if self.debug:
            print condicion
        res=self.leerCondicion(condicion, userId)

        #DEBUG
        if self.debug:
            print "Se ha retornado: "
            for doc in res:
                print doc
            #muy importante
            res.rewind()
        #Si se ha encontrado usuario. res.count() sera > 0.
        if res.count() > 0:
            #Existe usuario.
            #Ahora comprobamos contraseña
            #Obtenemos la contraseñña iterando por el resultado.
            #Si lo hacemos de otra manera, p.ej. res[0]["pass"]
            #nos devolverá u'pass' en lugar de pass
            contrasenna=None
            print "campo: " + str(self.campoPassword)
            for doc in res:
                print "iteracion: " + str(doc)
                print "iteracion pt2: " + str(doc[self.campoPassword])
                contrasenna=doc[self.campoPassword]
            
            if self.debug:
                print "pass buena: " + str(contrasenna)
                print "pass introducida: " + str(userPass)

            if contrasenna == userPass:
                #Usuario y contraseña correctos.
                #Añado el valor de la cookie y el usuario al
                #que corresponde.
                cookie=self.genCookieVal()
                entrada={cookie : userId}
                self.listaSesiones.update(entrada)
                #Consultando la cookie en este diccionario, nos
                #devolverá el usuario al que pertenece la cookie
                if self.debug:
                    print "todo correcto"
                return cookie

            else:
                if self.debug:
                    print "Contraseña incorrecta!"
                return -1
        else:
            if self.debug:
                print "No existe el usuario: " + userId
            return -1
    
    #Genera valor aleatorio para una cookie.
    #PLACEHOLDER
    def genCookieVal(self):
        return 0


if __name__ == "__main__":
    u = UserManager()
    u.borrar({})
    entrada = {u.campoUsername : "pablo" , u.campoPassword : "adios"}
    u.escribir(entrada)
    u.leer()
    userr = raw_input("user: ")
    passs = raw_input("pass: ")
    u.login(userr,passs)
