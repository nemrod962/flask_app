# -*- coding: utf-8 -*-
"""
This is a simple Flask app that uses Authomatic to log users in with Facebook
Twitter and OpenID.
"""

from flask import Flask, render_template, request, make_response, redirect, url_for, session
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from config_template import CONFIG

app = Flask(__name__)
#Needed by flask.session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# Instantiate Authomatic.
authomatic = Authomatic(CONFIG, 'your secret string', report_errors=False)

currentUser=None
currentResult=None

@app.route('/')
def index():
    """
    Home handler.
    """
    global currentUser

    try:
        temp=currentUser.name
    except AttributeError:
        temp=None

    return render_template('index.html', name=temp)


@app.route('/login/<provider_name>/', methods=['GET', 'POST'])
def login(provider_name):
    """
    Login handler, must accept both GET and POST to be able to use OpenID.
    """
    global currentUser
    global currentResult
    print "Empezando"
    # We need response object for the WerkzeugAdapter.
    response = make_response()

    # Log the user in, pass it the adapter and the provider name.
    result = authomatic.login(
        WerkzeugAdapter(
            request,
            response),
        provider_name)

    # If there is no LoginResult object, the login procedure is still pending.
    if result:
        #DEBUG
        print "result: " + str(result)
        print "provider: " + str(result.provider)
        print "user: " + str(result.user)
        print "error: " + str(result.error)
        if result.user:
            # We need to update the user to get more info.
            result.user.update()
            #---
            currentUser=result.user
            # The rest happens inside the template.
        #return render_template('login.html', result=result)
        #return redirect(url_for('index'))
        #No funciona pq LoginResult no es serializable por JSON
        #session['temp']=result
        currentResult=result
        return redirect(url_for('info'))

    """
    #No funciona. Una vez que se pasa a estar OFFLINE no
    #se recupera. Aunque vuelva la conexión seguirá indicando
    #que se stá sin conexión.
    if not result:
        print "offline"
        response=make_response("OFFLINE")
    """
    # Don't forget to return the response.
    return response

@app.route('/logininfo')
def info():
    #No funciona pq LoginResult no es serializable por JSON
    #resultado=session['temp']
    global currentResult
    resultado= currentResult
    return render_template('login.html', result=resultado)



# Run the app.
if __name__ == '__main__':
    app.run(debug=True, port=8080)
