"""
DIFERENTES PRUEBAS CON FLASK
"""
from flask import Flask, url_for, request, render_template, redirect
app = Flask(__name__) 

#Functions for different routes in the server
"""
@app.route("/") 
def index():
    return '<h1>Hello World!<h1>'
"""

@app.route("/loc")
def location():
    return '<p>Ubicacion: mi casa<p>'

@app.route('/desc/<sensor>')
def show_type(sensor=None):
    #return 'Tipo de sensor: %s' % sensor
    #print "Hola " + sensor
    #sens es una variable en el doc sensors.html
    return render_template('sensors.html', sens=sensor)

@app.route('/ver/<sen>/<v>')
def show_version(sen, v):
    return "Tipo de sensor: "+ sen + " | version: " + v 

@app.route('/vai/<int:val_i>')
def show_value_i(val_i):
    return "Valor del sensor: " + val_i

@app.route("/vaf/<float:val_f>")
def show_value_f(val_f):
    return "Valor del sensor: " + val_f

#REQUESTS
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do_the_login()'
    else:
        return 'show_the_login_form()'

#FORMULARIO

@app.route('/led', methods=['POST'])
def led():
    error = None
    if request.method == 'POST':
        color = resquest.form['color']
        if valid_color(color):
            change_color(color)
        else:
            error = 'Invalid color'
        return render_tmeplate('color.html', color=color, error=error)

@app.route("/") 
def my_form():
    #return render_template("my-form.html")
    return render_template("index.html")

@app.route("/", methods=['POST'])
def my_form_post():
    #text = request.form['text']
    text = request.form['option']
    processed_text = text.upper()
    #return processed_text
    sensor = "s1"
    return redirect(url_for('show_type', sensor="s1"))

@app.route("/submit",  methods=['GET'])
def submit():        
    nombre  =  request.args.get('Nombre',  'Anonymous')  
    return render_template('submit_result.html',  nombre=nombre,  metodo=request.method)

#URLS

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
    app.run(host='0.0.0.0')





