# -*- coding: utf-8 -*-
"""
OBTIENE EL PRIMER NUMERO ALEATORIO 
GENERADO POR LA PAGINA www.numeroalazar.com.ar
"""
#import requests #otra forma de obtener el cod fuente de una web
import urllib2
#regexp
import re

class Rnd_fetcher:

    #Atributo con la direccion de la web de la cual
    #se van a extraer los datos
    def __init__(self, dir = "http://www.numeroalazar.com.ar/", deb = False):
        self.web_dir = dir
        self.debug= deb

    #OBTIENE TODOS LOS NUMERO ALEATORIOS (CON CODIGO HTML ENTRE MEDIAS)
    def get_all_numbers(self, debug=False):
        #Activo el modo debug si la clase lo tiene activado
        if debug == False:
            debug = self.debug

        #get source
        try:
            response = urllib2.urlopen(self.web_dir)
        except:
            logging.warning("No se ha podido conectar a " + self.web_dir)
            return -1
        page_source = response.read()
        if debug:
            logging.debug(page_source)
            logging.debug("\n\n----------------\nREGEXP\n---------------------------")
        #regexp
        #OBTENER TODOS LOS NUMERO ALEATORIOS. PRUEBA:
        searchObj = re.findall('<div class="container"  id="numeros_generados">(.*?)</div>', page_source, re.S)
        """
        -> .* es GREEDY, intentará obtener el patron que conicida más largo. Esto no es lo que queremos, pues nos devolverá desde '<div class="conatiner... hasta el último </div> que encuentre en el código de la pag web. Para que nos devuelva la cadena que coindida hasta el primer </div> que encuentre tendremos que utilizar un patrón NON-GREEDY.
        ->.*? es NON-GREEDY
        -> esta bandera (re.S) hace que . tambien sustituya a \n.
        Sin ella, la expresion regular no funciona correctamente 
        """

        if debug:
            for line in searchObj:
                logging.debug("iteration---")
                logging.debug(line)

        return searchObj

    #OBTENER SOLO EL PRIMER NUMEROALEATORIO
    def get_web_rnd(self, debug=False):
        
        #Activo el modo debug si la clase lo tiene activado
        if debug == False:
            debug = self.debug

        #get source
        try:
            response = urllib2.urlopen(self.web_dir)
        except:
            logging.warning("No se ha podido conectar a " + self.web_dir)
            return -1
        #----
        page_source = response.read()
        if debug:
            logging.debug(page_source)
            logging.debug("\n\n----------------\nREGEXP\n---------------------------")
        searchObj = re.findall('<h2>Números generados</h2>(.*?)<br>', page_source, re.S)
        """
        -> .* es GREEDY, intentará obtener el patron que conicida más largo. Esto no es lo que queremos, pues nos devolverá desde '<div class="conatiner... hasta el último </div> que encuentre en el código de la pag web. Para que nos devuelva la cadena que coindida hasta el primer </div> que encuentre tendremos que utilizar un patrón NON-GREEDY.
        ->.*? es NON-GREEDY
        -> esta bandera (re.S) hace que . tambien sustituya a \n.
        Sin ella, la expresion regular no funciona correctamente 
        """

        for line in searchObj:
            if debug:
                logging.debug("iteration---")
            numero = float(line)
            if debug:
                logging.debug(line)
                logging.debug("NUMERO: ", numero)
        return numero


#Obtenemos un numero aleatorio si ejecutamos este .py
if __name__ == "__main__":
    clase =Rnd_fetcher()
    clase.get_web_rnd(True)

