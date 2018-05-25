# -*- coding: UTF-8 -*-
import gevent #para gevent.spawn
from Queue import Queue #Cola bloqueante
from threading import Thread #Hilos en vez de procesos

from flask import Flask, Response

import time
#logging
import logging
from log_handler import setup_log


class SSEHandler(object):
   
    #Variable de clase (estatica)
    #Compartida entre todas las instancias
    listaSubs = []

    #Añade SSE a las colas de los diferentes
    #suscriptores para que la funcion
    ##sendSSE se los envie
    def createSSE(self, msg=None):
        #Creo ~hilo que anadira el mensaje recibido a la lista
        #de los SSE a enviar
        if msg != None:
            gevent.spawn(self.__addEvent(msg))
        else:
            gevent.spawn(self.__addEvent())
        return "OK"
    

    #Cuando un cliente se suscriba, ejecutará esta función.
    def sendSSE(self):
        #Envio el SSE como respuesta. 
        return Response(self.__sendEvent(), mimetype="text/event-stream")

    #Devuelve el numero de suscriptores
    def getNumSuscriptores(self):
        return len(SSEHandler.listaSubs)
    
    #Privado. No puede llamarse desde fuera de la clase.
    def __addEvent(self, data="*empty message*"):
        msg=data
        logging.info("num suscriptores: " +\
            str(self.getNumSuscriptores()))
        for sub in SSEHandler.listaSubs:
            sub.put(msg)
        

    #Privado. No puede llamarse desde fuera de la clase.
    #Esta función es ejecutada cuando un cliente se suscribe.
    #Crea una cola, que será la cola de mensajes de ese cliente.
    #Contendrá los diferentes mensajes a enviarle.
    def __sendEvent(self):
        q = Queue()
        SSEHandler.listaSubs.append(q)
        logging.debug("SSEHandler - sendEvent():")
        logging.debug("listaSuscripciones: " + str(SSEHandler.listaSubs))
        try:
            while True:
                #q.get() espera hasta que haya elemento en q
                #CLAVE DEL FUNCIONAMIENTO. q.get() bloquea al
                #proceso hasta que la cola q contiene algun 
                #elemento.
                logging.debug("SSEHandler - Obteniendo SSE de la cola de suscriptores...")
                result = q.get()
                #result = "placeholder"
                ev = ServerSentEvent(str(result))
                yield ev.encode()
        #Se produce este error cuando se envía un SSE a un cliente que no está
        #disponible (no está escuvhando).
        #Cuando esto suceda, por la consola aparecerá el siguiente mensaje de 
        #error: 
		#----------------------------------------
		# SSEHandler - Obteniendo SSE de la cola de suscriptores...Exception happened during processing of request from
		# Conectando a Beebotte...SSEHandler - Obteniendo SSE de la cola de suscriptores...
		# 
		#('127.0.0.1', 46562)
		#Traceback (most recent call last):
		#  File "/usr/lib/python2.7/SocketServer.py", line 596, in process_request_thread
		#	self.finish_request(request, client_address)
		#  File "/usr/lib/python2.7/SocketServer.py", line 331, in finish_request
		#	self.RequestHandlerClass(request, client_address, self)
		#  File "/usr/lib/python2.7/SocketServer.py", line 654, in __init__
		#	self.finish()
		#  File "/usr/lib/python2.7/SocketServer.py", line 713, in finish
		#	self.wfile.close()
		#  File "/usr/lib/python2.7/socket.py", line 283, in close
		#	self.flush()
		#  File "/usr/lib/python2.7/socket.py", line 307, in flush
		#	self._sock.sendall(view[write_offset:write_offset+buffer_size])
		#error: [Errno 32] Broken pipe
		#----------------------------------------
		#Esto es un error conocido de Django, el cual no va a ser arreglado.
		#Informacion en el siguiente enlace: 
		#https://stackoverflow.com/questions/7912672/django-broken-pipe-in-debug-mode
		#Aunque se capture la excepcion, el mensaje descrito anteriormente seguirá saliendo en consola.
		#También se ha intentado ignorar la señal SIGPIPE con:
		#from signal import signal, SIGPIPE, SIG_DFL, SIG_IGN
		#signal(SIGPIPE,SIG_IGN) 
		#pero no ha dado resultado.
		#
		#FINALMENTE:
		#capturaremos esta excepción con 'except GeneratorExit'
        except GeneratorExit:
            logging.debug("*** Cliente desconectado.")
            SSEHandler.listaSubs.remove(q)
        except socket.error as e:
            logging.warning("socket error: " + str(e))
        except IOError as e:
            logging.warning("IO error: " + str(e))
        except:
            logging.warning("EXCEPTION UNKNOWN")


#Clase empleada para enviar los mensajes.
#En nuestro caso, simplemente rellenaremos el campo 'data' 
#y enviaremos el SSE.
# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
        #texto mensaje
        self.data = data
        #~grupo. tipo de evento.
        #En el cliente, con addEventListener(),
        #podemos especificar el tipo de evento al
        #que escuchar.
        self.event = None
        #The event ID to set the EventSource object's last event ID value.
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k)
                 for k, v in self.desc_map.iteritems() if k]

        return "%s\n\n" % "\n".join(lines)

