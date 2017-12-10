"""
OBTIENE NUMEROS ALEATORIOS JUNTO CON LA HORA Y FECHA
DE LA OBTENCION Y LOS ESCRIBE EN UN ARCHIVO
"""
import time #para sleep
import call_rnd as cr

def getDatos():
    #obtenemos resultado numero aleatorio
    entrada = cr.llamar_numero_aleatorio()
    return entrada

def initDatos():
    #abrimos archivo
    archivo = open("lista_random.txt", "a+")
    return archivo

#Le pasamos el fd del archivo en el que
#vamos a escribir
def writeDatos(archivo):
    #archivo = initDatos()
    datos = getDatos()
    archivo.write("\n---\n"+datos)

def __main__():
    archivo=initDatos()
    for i in xrange(3):
        print i
        writeDatos(archivo)
        time.sleep(2)
    archivo.close()
    print "Finished"

#ejecutar __main__():
__main__()

