"""
DIFERENTES PRUEBAS CON FLASK
"""
from flask import Flask, url_for, request, render_template, redirect,\
jsonify, make_response

app = Flask(__name__) 

#Functions for different routes in the server
@app.route("/", methods = ['GET','POST']) 
def index():
    if request.method == 'GET':
        return render_template("ejemplo.html")
    else:
        redir = url_for('index')
        data = {'dir': redir, 'code': 0}

        response = make_response(jsonify(data))
        response.set_cookie("valor_cookie","1")
        return response

@app.route("/ejemplo") 
def test():
    return render_template("index.html")


"""
#Estas lineas hacen que funcione url_for pero 
#hacen el servicor inaccesible desde el navegador
app.config['SERVER_NAME'] = 'localhost'
with app.app_context():
    url1 = url_for('location')
    url2 = url_for('show_type', sensor = 'sen1')
    url3 = url_for('static', filename='style.css')

print(url1)
print(url2)
print(url3)
"""

#LAUNCH APP
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)


