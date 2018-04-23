from padre import Padre

class Hijo(Padre):
    def __init__(self):
        super(Hijo, self).__init__()
        #self.atr0=9
        self.atr2="Hijo"

    def getAtr2(self):
        return self.atr2

    def mostrar(self):
        print "atr0: " + str(self.getAtr0())
        print "atr1: " + str(self.getAtr1())
        print "atr2: " + str(self.getAtr2())
    
    #Sobrescribo funcion padre
    def func1(self, n):
        print "Soy la func1() del hijo:"
        print "QWE"

if __name__ == "__main__":
    h = Hijo()
    h.mostrar()
