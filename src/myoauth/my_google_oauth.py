# -*- coding: utf-8 -*-
"""
Clase que se encarga de la Autenticación por OAuth2 de Google.
Será utilizada por la clase UserManager en mongo_user.py para
obtener credenciales (nombre, id y e-mail).
Con estas credenciales
"""
#Librerías Authomatic para OAuth
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic
#Configuración del fichero config_template
from config_template import CONFIG
#Utilizado en gedOAuthCredntials()
from flask import make_response

#PREUBAS
from flask import Flask, render_template, request, redirect, url_for, session



#--------------------------------------------------------------------------------------------
class OAuthHandler:

    def __init__(self, debug=False):
        #Instancia de la clase Authomatic. La utilizo para realizar
        #la autenticación mediante OAuth
        self.debug=debug
        self.automatico = Authomatic(CONFIG, 'SECRET_STRING_$%&', report_errors=self.debug)
        
    """
    Devuelvo un diccionario como resultado de realizar la autenticación
    mediante OAuth. Tendrá las siguientes claves:
        -> nombre : contiene el nombre del usuario
        -> correo : contiene la dirección del usuario
        -> id : contiene el id único del usuario
    """
    def getOAuthCredentials(self):
        
        #Diccionario que retornaremos con los datos
        oauthData=dict()
        
        # We need response object for the WerkzeugAdapter.
        response = make_response()
        
        #Hacemos OAuth2 en Google
        provider_name="google"

        # Log the user in, pass it the adapter and the provider name.
        result = self.automatico.login(
            WerkzeugAdapter(request,response),\
            provider_name)

        #DEBUG
        print "DEBUG: result - " + str(result)

        # If there is no LoginResult object, the login procedure is still pending.
        if result:
            #DEBUG
            if self.debug:
                print "result: " + str(result)
                print "provider: " + str(result.provider)
                print "user: " + str(result.user)
                print "error: " + str(result.error)
            if result.user:
                print "Hay result.user"
                #NECESARIO PARA OBTENER INFORMACION
                result.user.update()
                oauthData['nombre'] = result.user.name
                oauthData['correo'] = result.user.email
                oauthData['id'] = result.user.id
                print "AAAAAAAAAAAAAAA: " + str(oauthData)
            return str(oauthData)
        #return response 

#--------------------------------------------------------------------------------------------

if __name__ == '__main__':
    c = OAuthHandler(True)
    d=c.getOAuthCredentials()

