#Para pasar por referencia
class OAuthRes:
    def __init__(self, d="noninit"):
        self.data=d
    def getData(self):
        return self.data
    def setData(self, data):
        self.data=data
    def getDataType(self):
        return str(type(self.data))
    def __str__(self):
        return str(self.data)

