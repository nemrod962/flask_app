# Author: Gouthaman Balaraman
# http://gouthamanbalaraman.com/minimal-flask-login-example.html

from flask import Flask, Response, redirect, url_for
from flask.ext.login import LoginManager, UserMixin, login_required
from flask import session

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)

#diccionario sesion
#session = {}

#SESSIONTRAVKING---------------------------------
#app.config['SECRET_KEY'] = 'any random string' #must be set to use sessions
#set session
@app.route('/login')
def login_success():
    global session
    session['key_name'] = 'key_value' #stores a secure cookie in browser
    return redirect(url_for('index'))
#read session
@app.route('/')
def index():
    if 'key_name' in session: #session exists and has key
        session_var = session['key_name'] 
        return "SESSION: " + session_var
    else: #session does not exist
        return "NO SESSION"



if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    #app.run(port=5000,debug=True)
    print "try: http://192.168.153.128:5000/protected/?token=JohnDoe:John"
    app.run(host='0.0.0.0',port=5000,debug=True)
