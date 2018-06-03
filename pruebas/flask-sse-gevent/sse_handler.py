# -*- coding: UTF-8 -*-
import gevent
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue

from flask import Flask, Response

import time

class SSEHandler(object):
	
	#lista con las colas que contendran los mensajes a enviar
	#Es un atributo de clase, no de instancia, por
	#eso va fuera del __init__()
	#listaSuscripciones = []
	#INIT
	def __init__(self):
		self.listaSuscripciones = []

	def createSSE(self, msg="*empty message*"):
		#Creo ~hilo que anadira el mensaje recibido a la lista
		#de los SSE a enviar
		gevent.spawn(self.__addEvent(msg))
		return "OK"

	def sendSSE(self):
		return Response(self.__sendEvent(), mimetype="text/event-stream")

	
	#Privado. No puede llamarse desde fuera de la clase.
	def __addEvent(self, data="placeholder"):
		msg=data
		#for sub in SSEHandler.listaSuscripciones:
		for sub in self.listaSuscripciones:
			sub.put(msg)
		

	#Privado. No puede llamarse desde fuera de la clase.
	def __sendEvent(self):
			q = Queue()
			#SSEHandler.listaSuscripciones.append(q)
			self.listaSuscripciones.append(q)
			print "q: " + str(q)
			#print "listaSuscripciones: " + str(SSEHandler.listaSuscripciones)
			print "listaSuscripciones: " + str(self.listaSuscripciones)
			try:
				while True:
					#q.get() espera hasta que haya elemento en q
					#gevent.queue implementa colas sincronizadas 
					#(se comparten entre procesos).
					#CLAVE DEL FUNCIONAMIENTO. q.get() bloquea al
					#proceso hasta que la cola q contiene algun 
					#elemento.
					print "Obteniendo elemento de la cola..."
					result = q.get()
					#result = "placeholder"
					ev = ServerSentEvent("SSE: "+str(result))
					yield ev.encode()
			#Se produce este error cuando se envía un SSE a un cliente que no está
			#disponible (no está escuvhando).
			except GeneratorExit:
				print "No se pudo entregar a un cliente suscrito."
				#SSEHandler.listaSuscripciones.remove(q)
				self.listaSuscripciones.remove(q)


#Clase empleada para enviar los mensajes.
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

