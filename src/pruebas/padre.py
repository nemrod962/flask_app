class Padre(object):

    def __init__(self):
        self.atr0=0
        self.atr1="Padre"
    
    def getAtr0(self):
        return self.atr0

    def getAtr1(self):
        return self.atr1

    def func1(self, n):
        print "Soy func1, del padre. Sumo 1."
        print str(n) + "+ 1 = " + str(n+1)

    def llamar(self, n):
        print "padre - llamando funcion func1("+str(n)+")"
        self.func1(n)
