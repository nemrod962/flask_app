# -*- coding: utf-8 -*-
from interface_rnd import HandlerInterface

class prueba(HandlerInterface):

    def __init__(self,a=1):
        HandlerInterface.__init__(self)
        self.a=a

    def writeRandom(self,a,b):
        print "parametro a: " + str(a)
        self.listaGlobalNumero.append(a)
        print "parametro b: " + str(b)
        self.listaGlobalFecha.append(b)

    def readRandom(self):
        print "Lista Num"
        print self.listaGlobalNumero
        print "Lista dato"
        print self.listaGlobalFecha



if __name__ == "__main__":

    asd = prueba()
