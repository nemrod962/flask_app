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
    #OBTIENE TODOS LOS NUMERO ALEATORIOS (CON CODIGO HTML ENTRE MEDIAS)
    def get_all_numbers(self):
        #get source
        response = urllib2.urlopen("http://www.numeroalazar.com.ar/")
        page_source = response.read()
        print page_source
        print "\n\n----------------\nREGEXP\n---------------------------"
        #regexp
        #OBTENER TODOS LOS NUMERO ALEATORIOS. PRUEBA:
        searchObj = re.findall('<div class="container"  id="numeros_generados">(.*?)</div>', page_source, re.S)
        """
        -> .* es GREEDY, intentará obtener el patron que conicida más largo. Esto no es lo que queremos, pues nos devolverá desde '<div class="conatiner... hasta el último </div> que encuentre en el código de la pag web. Para que nos devuelva la cadena que coindida hasta el primer </div> que encuentre tendremos que utilizar un patrón NON-GREEDY.
        ->.*? es NON-GREEDY
        -> esta bandera (re.S) hace que . tambien sustituya a \n.
        Sin ella, la expresion regular no funciona correctamente 
        """
        #searchObj = re.findall('<div(.*)</div>', page_source, re.I | re.S)

        for line in searchObj:
            print "iteration---"
            print line

    #OBTENER SOLO EL PRIMER NUMEROALEATORIO
    def get_web_rnd(self, debug=False):
        #get source
        response = urllib2.urlopen("http://www.numeroalazar.com.ar/")
        page_source = response.read()
        if debug:
            print page_source
            print "\n\n----------------\nREGEXP\n---------------------------"
        searchObj = re.findall('<h2>Números generados</h2>(.*?)<br>', page_source, re.S)
        """
        -> .* es GREEDY, intentará obtener el patron que conicida más largo. Esto no es lo que queremos, pues nos devolverá desde '<div class="conatiner... hasta el último </div> que encuentre en el código de la pag web. Para que nos devuelva la cadena que coindida hasta el primer </div> que encuentre tendremos que utilizar un patrón NON-GREEDY.
        ->.*? es NON-GREEDY
        -> esta bandera (re.S) hace que . tambien sustituya a \n.
        Sin ella, la expresion regular no funciona correctamente 
        """

        for line in searchObj:
            if debug:
                print "iteration---"
            numero = float(line)
            if debug:
                print line
                print "NUMERO: ", numero
        return numero

