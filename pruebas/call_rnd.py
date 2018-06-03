"""
LLAMA A LA FUNCION RND_FETCHER() DEL
FICHERO RND_FETCHER.PY PARA OBTENER
UN NUMERO ALEATORIO DE LA WEB.

DEVUELVE UNA STRING CON EL NUMERO ALEATORIO
JUNTO CON LA HORA Y LA FECHA
"""
#import rnd_fetcher
#clase=rnd_fetcher.Rnd_fetcher()
import time
import web_fetcher.rnd_fetcher as cla

def llamar_numero_aleatorio():
    #numero aleatorio
    clase = cla.Rnd_fetcher()
    rnd = clase.get_web_rnd()
    #fecha
    fecha = time.strftime("%d/%m/%Y")
    #hora
    hora = time.strftime("%H:%M:%S")

    return "rnd: "+str(rnd)+"\nfecha: "+fecha+"\nhora: "+hora
