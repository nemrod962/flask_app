"""
DIFERENTES PRUEBAS CON FLASK
"""
from flask import Flask, url_for, request, render_template, redirect
app = Flask(__name__) 

#Functions for different routes in the server
@app.route("/") 
def test():
    return render_template("template.html")

#LAUNCH APP
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)


