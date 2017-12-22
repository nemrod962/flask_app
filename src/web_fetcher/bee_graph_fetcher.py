# -*- coding: UTF-8 -*-
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib2

#Accede a la dirección donde se encuentra
#el dashboard de Beebotte que he creado
#donde se encuentran las gráficas de la 
#variable que se almacena alli.
#Abro esa dirección con phantomJS para
#ejecutar el código de javascript que 
#genera las gráficas. Una vez que
#disponemos de todo el código html de 
#la página, gráficas incluidas, nos
#quedamos únicamente con las gráficas
#gracias a BeautifulSoup.
#Retornamos el código html de las gráficas
def getGraphHTML(debug=False):
    if debug:
        print "GO!"
    url = "https://beebotte.com/dash/"
    tablaID = "09db3e70-df3a-11e7-bfef-6f68fef5ca14"
    fullurl = url+tablaID
    if debug:
        print fullurl

    driver = webdriver.PhantomJS()
    driver.get(fullurl)
    #page_source fetches page after rendering is complete
    soup = BeautifulSoup(driver.page_source, "html.parser")
    widgetsID = tablaID+"_body"
    if debug:
        print widgetsID
    res = soup.find_all(id=widgetsID)
    if debug:
        print res
    driver.save_screenshot('screen.png') # save a screenshot to disk
    #Finalizo el driver
    driver.quit()
    return res
