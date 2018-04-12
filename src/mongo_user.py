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
#Para generacion de cookies
#base64
import base64
#para hashes
from passlib.hash import pbkdf2_sha256
#para numeros aleatorios
import random
#Para comprobar si un objeto es un numero de cualq tipo
from numbers import Number
#Herencia de la clase base para trabajar con MongoDB
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

    """
     _                _          ___     _                            _   
    | |    ___   __ _(_)_ __    ( _ )   | |    ___   __ _  ___  _   _| |_ 
    | |   / _ \ / _` | | '_ \   / _ \/\ | |   / _ \ / _` |/ _ \| | | | __|
    | |__| (_) | (_| | | | | | | (_>  < | |__| (_) | (_| | (_) | |_| | |_ 
    |_____\___/ \__, |_|_| |_|  \___/\/ |_____\___/ \__, |\___/ \__,_|\__|
                |___/                               |___/                 
    """

    #Login.
    #Verifica si el usuario indicado existe.
    #De ser así, devuelve el valor de la cookie para la 
    #sesion actual del usuario.
    #Si el usuario indicado no existe, o la contraseña es
    #incorrecta, devolveremos -1.
    def login(self, userId, userPass):
        #COMPROBACIONES DATOS
        #compruebao tipos de datos
        if not isinstance(userId, str) or not isinstance(userPass, str):
            if self.debug:
                print "El usuario y la contraseña deben ser strings!"
            return -1
        #compruebo longitud nbombre y pass
        if len(userId) < 4 or len(userPass) < 4:
            if self.debug:
                print "El usuario y la contraseña deben" + \
                "ser de al menos 4 chars de longitud!"
            return -1

        #REALIZO OPERACIONES PARA LOGIN
        condicion={self.campoUsername : userId}
        if self.debug:
            print condicion
        res=self.leerCondicion(condicion, userId)

        #DEBUG
        if self.debug:
            print "Con user: " + str(userId)
            print "Se ha encontrado el usuario: "
            for doc in res:
                print doc
            #muy importante
            res.rewind()
        #Si se ha encontrado usuario. res.count() sera > 0.
        if res.count() > 0:
            #Existe usuario.
            #Ahora comprobamos contraseña
            #Obtenemos el has de la contraseña iterando por el resultado.
            #Si lo hacemos de otra manera, p.ej. res[0]["pass"]
            #nos devolverá u'pass' en lugar de pass
            hashPass=None
            for doc in res:
                if self.debug:
                    #print "iteracion: " + str(doc)
                    #print "iteracion pt2: " + str(doc[self.campoPassword])
                    print ""
                hashPass=doc[self.campoPassword]
            
            #Comparamos la contraseña introducida con el
            #hash de la contraseña verdadera
            correctPass = pbkdf2_sha256.verify(userPass , hashPass)

            #DEBUG
            if self.debug:
                print "hash pass buena: " + str(hashPass)
                print "pass introducida: " + str(userPass)
                print "Coinciden? : " + str(correctPass)

            if correctPass:
                #Usuario y contraseña correctos.
                #Añado el valor de la cookie y el usuario al
                #que corresponde.
                cookie=self.genCookieVal(userId)
                entrada={cookie : userId}
                self.listaSesiones.update(entrada)
                #Consultando la cookie en este diccionario, nos
                #devolverá el usuario al que pertenece la cookie
                if self.debug:
                    print "Sesion iniciada. Id: " + str(cookie)
                return cookie

            else:
                if self.debug:
                    print "Contraseña incorrecta!"
                return -1
        else:
            if self.debug:
                print "No existe el usuario: " + userId
            return -1
    #Logout.
    #Devuelve 0 si se ha salido de la sesión correctamente
    #Devuelve -1 si la sesiónde la que se ha intentado salir
    #no existía.
    def logout(self, cookieVal):
        try:
            del self.listaSesiones[cookieVal]
            return 0
        except KeyError as e:
            if self.debug:
                print "Se ha intentado salir de una sesion que no existe: "\
                + str(cookieVal)
            return -1

    """
      ____                _          ___     ____       _      _       
     / ___|_ __ ___  __ _| |_ ___   ( _ )   |  _ \  ___| | ___| |_ ___ 
    | |   | '__/ _ \/ _` | __/ _ \  / _ \/\ | | | |/ _ \ |/ _ \ __/ _ \
    | |___| | |  __/ (_| | ||  __/ | (_>  < | |_| |  __/ |  __/ ||  __/
     \____|_|  \___|\__,_|\__\___|  \___/\/ |____/ \___|_|\___|\__\___

     _   _                   
    | | | |___  ___ _ __ ___ 
    | | | / __|/ _ \ '__/ __|
    | |_| \__ \  __/ |  \__ \
     \___/|___/\___|_|  |___/
                     
    """
    #Crea un usuario con los parámetros especificados.
    #El valor -1 para umbral significa que el usuario no quiere
    #notificaciones para umbrales.
    def createUser(self, userId, userPass, umbral=-1):
        #COMPROBACIONES DATOS
        #compruebo tipos de datos
        if not isinstance(userId, str) or not isinstance(userPass, str):
            if self.debug:
                print "El usuario y la contraseña deben ser strings!"
            return -1
        if not isinstance(umbral, Number):
            if self.debug:
                print "El umbral debe ser un número!"
            return -1
        #CREAR USUARIO    
        #compruebo longitud nombre y pass
        if len(userId) < 4 or len(userPass) < 4:
            if self.debug:
                print "El usuario y la contraseña deben" + \
                "ser de al menos 4 chars de longitud!"
            return -1
        #comprobamos que el nombre del usuario no existe
        condicion={self.campoUsername : userId}
        res=self.leerCondicion(condicion, userId)
        #DEBUG
        if self.debug:
            print "Con user: " + str(userId)
            print "Se ha encontrado el usuario: "
            for doc in res:
                print doc
            #muy importante
            res.rewind()

        #Si se ha encontrado usuario. res.count() sera > 0.
        if res.count() > 0:
            #Existe usuario. Aborto misión.
            #Salimos con código de error.
            return -1
        else:
            #generamos has de la contraseña, que sera lo que guardemos.
            hashPass = pbkdf2_sha256.hash(userPass)
            #generamos los datos del usuario a almacenar
            datos = {self.campoUsername : userId , \
            self.campoPassword : hashPass, \
            self.campoUmbral : umbral}
            #escribimos datos de usuario en MongoDB
            res=self.escribir(datos)
            #Retornamos 0 en caso de escciribir los datos satisfactoriamente
            return res

    #Borrar Usuario.
    #Verifica si el usuario indicado existe.
    #Si el usuario indicado no existe, o la contraseña es
    #incorrecta, devolveremos -1.
    def deleteUser(self, userId, userPass):
        
        #COMPROBACIONES DE LO DATOS
        #compruebo tipos de datos
        if not isinstance(userId, str) or not isinstance(userPass, str):
            if self.debug:
                print "El usuario y la contraseña deben ser strings!"
            return -1
        #compruebo longitud nombre y pass
        if len(userId) < 1 or len(userPass) < 1:
            if self.debug:
                print "El usuario y la contraseña deben" + \
                "ser de al menos 1 char de longitud!"
            return -1

        #BORRAR USUARIO
        condicion={self.campoUsername : userId}
        if self.debug:
            print condicion
        res=self.leerCondicion(condicion, userId)

        #DEBUG
        if self.debug:
            print "Con user: " + str(userId)
            print "Se ha encontrado el usuario: "
            for doc in res:
                print doc
            #muy importante
            res.rewind()
        #Si se ha encontrado usuario. res.count() sera > 0.
        if res.count() > 0:
            #Existe usuario.
            #Ahora comprobamos contraseña
            #Obtenemos el has de la contraseña iterando por el resultado.
            #Si lo hacemos de otra manera, p.ej. res[0]["pass"]
            #nos devolverá u'pass' en lugar de pass
            hashPass=None
            for doc in res:
                if self.debug:
                    #print "iteracion: " + str(doc)
                    #print "iteracion pt2: " + str(doc[self.campoPassword])
                    print ""
                hashPass=doc[self.campoPassword]
            
            #Comparamos la contraseña introducida con el
            #hash de la contraseña verdadera
            correctPass = pbkdf2_sha256.verify(userPass , hashPass)

            #DEBUG
            if self.debug:
                print "hash pass buena: " + str(hashPass)
                print "pass introducida: " + str(userPass)
                print "Coinciden? : " + str(correctPass)

            if correctPass:
                #Usuario y contraseña correctos.
                #Procedo a borrar el usuario
                res=self.borrar(condicion)
                return res

            else:
                if self.debug:
                    print "Contraseña incorrecta!"
                return -1
        else:
            if self.debug:
                print "No existe el usuario: " + userId
            return -1
    """
    MISC
    """
    #Genera valor aleatorio para una cookie.
    #PLACEHOLDER
    def genCookieVal(self, userId):
        repetir=True
        while repetir:
            #La cookie consistirá en el nombre de usuario seguido de un
            #número aleatorio entre 0 y 1000000.
            #Todo ello será codificado en base64
            prefijo = random.randint(0,1000000)
            cookiePre=str(userId)+str(prefijo)
            #DEBUG
            if self.debug:
                print "Cookie sin codificar: " + str(cookiePre)
            cookie=base64.b64encode(cookiePre)
            #HAY QUE COMPROBAR SI YA EXISTE ESE VALOR EN LISTASESIONES
            #Si ya existe, generop de nuevo la clave
            #SI no (lo normal), salgo y retorono la cookie
            if not (cookie in self.listaSesiones):
                repetir=False
        #retorno la cookie
        return cookie

    #Modificar valor umbral para un usuario
    #Dado un usuario y un valor para el umbral, asignaremos ese
    #umbral al usuario. El umbral debe estar comprendido entre 0 y 100.
    def modUmbral(self, userId, umbral):
        #COMPROBACION TIPOS
        #nombre usuario valido
        if not ( isinstance(userId, str) and len(userId)>0 ):
            if self.debug:
                print "modUmbral : Tipo y/o longitud de usuario no válido."
            return -1
        #umbral valido
        if not ( isinstance(umbral, Number) and umbral >=0 \
        and umbral <=100 ):
            if self.debug:
                print "modUmbral : Tipo y/o valor de umbral no válido."+ \
                "El valor del umbral debe estar comprendido entre 0 y 100."
            return -1
        
        #MODIFICACION UMBRAL
        #busco usuario indicado
        condicion={self.campoUsername : userId}
        #DEBUG
        if self.debug:
            print condicion
        #Obtengo el resultado de búsqueda de usuario en res    
        res=self.leerCondicion(condicion, userId)

        #DEBUG
        if self.debug:
            print "Con user: " + str(userId)
            print "Se ha encontrado el usuario: "
            for doc in res:
                print doc
            #muy importante hacer rewind
            res.rewind()
        #Si se ha encontrado usuario. res.count() sera > 0.
        if res.count() > 0:
            #Existe usuario. Procedo a modificar el umbral.
            #creo la asignacion. La condicion ya la tengo declarada.
            asignacion={ self.campoUmbral : umbral }
            #Actualizo valor en MongoDB
            res = self.actualizar(condicion, asignacion)
            return res
        else:
            if self.debug:
                print "No se ha encontrado el usuario: " + str(userId)
            return -1
            


            
if __name__ == "__main__":

    #Funcion privada para parsear strings a numeros
    def num(s):
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return None
    #----------------------------------------------
    u = UserManager()
    u.deleteUser("asd", "asd")
    """ 
    print "Crear:"
    userr = raw_input("user: ")
    passs = raw_input("pass: ")
    u.createUser(userr, passs)
    """
    u.leer()
    print "Login:"
    userr = raw_input("user: ")
    passs = raw_input("pass: ")
    u.login(userr,passs)
    
    u.leer()
    userr = raw_input("user: ")
    umbrall = raw_input("umbral: ")
    umbrall=num(umbrall)
    #userr = 123
    #umbrall = 12L
    res=u.modUmbral(userr, umbrall)
    print "modUmbral : " + str(res)
    u.endConn()
