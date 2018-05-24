from flask import Blueprint, render_template, url_for

vista1 = Blueprint('vista1', __name__, 
template_folder='templates', static_folder='static')

@vista1.route('/')
def index():
    return "Vista1 MAIN"

@vista1.route('/page')
def show():
        cadena = url_for("static", filename="styles/style.css")
        print "URLFOR /static:" + cadena
        cadena2 = url_for(".index")
        print "URLFOR index(): " + cadena2
        return render_template('template.html')

def suma(a,b):
    return a+b
