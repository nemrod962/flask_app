from flask import Blueprint, render_template, url_for
from blue1 import suma

vista2 = Blueprint('vista2', __name__, 
template_folder='templates', static_folder='static')

@vista2.route('/2')
def index():
    print "1 + 2: " + str(suma(1,2))
    return "Vista2 MAIN"

@vista2.route('/page2')
def show():
        cadena = url_for("static", filename="styles/style.css")
        print "URLFOR /static:" + cadena
        cadena2 = url_for(".index")
        print "URLFOR index(): " + cadena2
        return render_template('template.html')
