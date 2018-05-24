# -*- coding: utf-8 -*-
import sys
import logging

"""
def setup_log_bk(debug=False):
    #Setup log
    logfile="log.txt"
    formato = '%(asctime)s - %(levelname)s - %(message)s'
    #limpio archivo log
    logging.FileHandler(logfile, mode='w')
    logging.basicConfig(filename=logfile, format=formato, level=logging.DEBUG)
    logging.info("probando")
    mlog = logging.getLogger()
    #Añado al log todos los mensajes
    mlog.setLevel(logging.DEBUG)
    level = logging.INFO

    if debug:
        level = logging.DEBUG

    #En caso de elegir modo debug, también
    #mostraré los mensajes de log por la terminal
    ch=logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    formatter = logging.Formatter(formato)
    ch.setFormatter(formatter)
    mlog.addHandler(ch)
"""

formato = "%(asctime)s - %(levelname)s -" + \
" linea %(lineno)d>%(module)s.%(funcName)s() : %(message)s"

def setup_log(debug=False):
    #Setup log
    logfile="log.txt"
    #limpio archivo log
    logging.FileHandler(logfile, mode='w')
    logging.basicConfig(filename=logfile, format=formato, level=logging.DEBUG)
    logging.info("probando")

    #default
    level = logging.INFO

    #setLogMode(level)
    initStreamMode(level, formato)

def setLogMode(level):
    if level == logging.DEBUG \
    or level == logging.INFO \
    or level == logging.WARNING:
        log = logging.getLogger()
        log.setLevel(level)

#Añado StreamHandler a logging
#para mostrar logs por pantalla
def initStreamMode(level, \
forma = formato):
    if level == logging.DEBUG \
    or level == logging.INFO \
    or level == logging.WARNING:
        ch=logging.StreamHandler(sys.stdout)
        ch.setLevel(level)
        formatter = logging.Formatter(forma)
        ch.setFormatter(formatter)
        log = logging.getLogger()
        log.addHandler(ch)

#Cambio nivel de sensibilidad del 
#StreamHandler
def setStreamMode(level):
    if level == logging.DEBUG \
    or level == logging.INFO \
    or level == logging.WARNING:
        log = logging.getLogger()
        for i in log.handlers:
            if str(i.__class__.__name__) == "StreamHandler":
                i.setLevel(level)
