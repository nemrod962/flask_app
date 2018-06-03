"""
PRUEBA PARA TRABAJAR CON MYSQL-FLASK
INSERTA UNA TUPLA EN LA TABLA tablaprueba
YA DEFINIDA Y MUESTRA TODAS LAS FILAS DE 
LA MISMA
"""
from flask import Flask
from flaskext.mysql import MySQL

app = Flask(__name__)

@app.route("/")
def default_function():
    return "Hello_World!"

def hola():
    print "hola"

hola()

#SQL CONFIG
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'lab'
app.config['MYSQL_DATABASE_PASSWORD'] = 'ubuntu16'
app.config['MYSQL_DATABASE_DB'] = 'myFlaskDB'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
#SQL INIT
mysql.init_app(app)
conn=mysql.connect()
cursor=conn.cursor()

#launch queries
cursor.execute('''insert into tablaprueba values (2,'insertado_desde_flask')''')
cursor.execute('''SELECT * FROM tablaprueba''')
res=cursor.fetchall()
print "Datos obtenidos (o no)"
print res


#LAUNCH FLASK
if __name__ == "__main__":
    app.run(host='0.0.0.0')

