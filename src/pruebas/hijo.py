from padre import Padre

class Hijo(Padre):
    def __init__(self):
        Padre.__init__(self)
        #self.atr0=9
        self.atr2="Hijo"

    def getAtr2(self):
        return self.atr2

    def mostrar(self):
        print "atr0: " + str(self.getAtr0())
        print "atr1: " + str(self.getAtr1())
        print "atr2: " + str(self.getAtr2())

if __name__ == "__main__":
    h = Hijo()
    h.mostrar()
