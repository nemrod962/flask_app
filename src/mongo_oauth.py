# -*- coding: utf-8 -*-
"""
Clase encargada de guardar y consultar los usuarios registrados
mediante OAuht almacenados en MongoDB.

Estructura de los documentos almacenando usuarios en MongoDB
Campos:
    -> username: nombre de usuario
    -> email: email del usuario (opcional).
    -> id: identificador único del usuario.
    -> provider: Entidad de la que he obtenido los datos (Google).
    -> umbral: Si se obtiene un numero aleatorio
        superior al umbral,se le
        notificara al usuario.

Hereda de la clase de guardar los usarios en MongoDB ya que muchas
de las operaciones a realizar son similares o iguales.

IMPORTANTE: Reconsiderar si en vez de heredar de UserManager es preferible que
heredo de MongoBasic, de forma que parte de su funcionalidad se la relegue a
User Manager, ya que él ya la tiene implementada y de forma que se tengan los
datos de usuarios en el mismo sitio.
"""

def OAuthUserManager(UserManager):
    
    #Constructor
    #Recibiré una instancia de UserManager, de forma que en vez de tener listas
    #de sesión locales, trabajaré con las de la instancia de UserManager
    #recibida como parámetro, de forma que tendré toda la información de las
    #sesiones unificada.
    def __init__(self, coleccionUsuariosOauth="usuariosOauth",\
    mongoUserManager=None, debug=True):
        #Igual que el de el padre pero cambiando la coleccion empleada
        super.__init__(self,coleccionUsuariosOauth,debug)
        #Añadimos los campos que no tenia el padre
        self.campoProveedor="provider"
        self.campoEmail="email"
        #
        #SOBRESCRIBO el campo 'username' por el campo id,
        #ya que en mongo_user se empleaba este campo como
        #clave primaria y en esta clase empleare la id como
        #clave primaria, como si fuera el nombre de usuario.
        #
        #El campo campoUsername se emplea en funciones como
        #modUmbral para cambiar el umbral del usuario. Como esas
        #funciones no necesito cambiarlas, sobrescribiré el campo
        #de forma que se utilice el id para buscar el usuario y no
        #el username.
        self.campoUsername="id"
        #Los campos que siguen igual son los de password (no se
        #utiliza) y el de umbral.

        #trabajaré con las listas de sesiones de la instancia de UserManager
        #recibida como parámetro, de forma que tendré toda la información de las
        #sesiones unificada.
        self.mongoUserManager=mongoUserManager


    """
     _                _          ___     _                            _   
    | |    ___   __ _(_)_ __    ( _ )   | |    ___   __ _  ___  _   _| |_ 
    | |   / _ \ / _` | | '_ \   / _ \/\ | |   / _ \ / _` |/ _ \| | | | __|
    | |__| (_) | (_| | | | | | | (_>  < | |__| (_) | (_| | (_) | |_| | |_ 
    |_____\___/ \__, |_|_| |_|  \___/\/ |_____\___/ \__, |\___/ \__,_|\__|
                |___/                               |___/                 
    """
    #Login.
    #El usuario se identificará por su id única aportada
    #por el proveedor.
    #Verifica si el usuario indicado existe.
    #De ser así, devuelve el valor de la cookie para la 
    #sesion actual del usuario.
    #Si el usuario indicado no existe, devolveremos -1.
    #Solo indicamos el nombre de usuario ya que 
    #la autenticación ya se ha realizado mediante OAuth
    def login(self, userId):
        


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

    """
      ____            _    _           
     / ___|___   ___ | | _(_) ___  ___ 
    | |   / _ \ / _ \| |/ / |/ _ \/ __|
    | |__| (_) | (_) |   <| |  __/\__ \
     \____\___/ \___/|_|\_\_|\___||___/
                                        
    """

    """
     __  __ _              _                        
    |  \/  (_)___  ___ ___| | __ _ _ __   ___  ___  
    | |\/| | / __|/ __/ _ \ |/ _` | '_ \ / _ \/ _ \ 
    | |  | | \__ \ (_|  __/ | (_| | | | |  __/ (_) |
    |_|  |_|_|___/\___\___|_|\__,_|_| |_|\___|\___/ 
    """

    #@OVERRIDE
    #EXISTE USUARIO. No cambio el nombre para hacer override, de
    #forma que cuando ejecute funciones heredadas del padre y estas
    #llamen a la funcion checkUserName, se ejecute esta funcion y 
    #no la original del padre.
    #Dado el id de un usuario comprueba si existe en la base de
    #datos de MongoDB.
    #Devuelve True si existe ese Id de Usuario,
    #False en caso contrario
    def checkUserName(self, userId):
        condicion={self.campoId : userId}
        """
        if self.debug:
            print condicion
        """
        res=self.leerCondicion(condicion, userId)
        #DEBUG
        if self.debug:
            print "MongoOauth - Con Id: " + str(userId)
            print "Se ha encontrado el usuario: "
            for doc in res:
                print doc
            #muy importante
            res.rewind()
        #Si se ha encontrado usuario. res.count() sera > 0.
        return res.count() > 0
    
                                                 

