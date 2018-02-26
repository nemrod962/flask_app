from flask import Flask, session, redirect, url_for, escape, request

app = Flask(__name__)

@app.route('/')
def index():
    if 'username' in session:
        username = session['username']
        return 'Logged in as ' + username + '<br>' + \
            "<b><a href = '/logout'>click here to log out</a></b>"
    return "You are not logged in <br><a href = '/login'></b>" + \
        "click here to log in</b></a>"


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''

    <form action = "" method = "post">
    <p><input type = "text" name = "username"/></p>
    <p><input type = "submit" value = "Login"/></p>
    </form>

    '''
@app.route('/logout')
def logout():
# remove the username from the session if it is there
    session.pop('username', None)
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.config["SECRET_KEY"] = "ITSASECRET"
    #app.run(port=5000,debug=True)
    print "try: http://192.168.153.128:5000/protected/?token=JohnDoe:John"
    app.run(host='0.0.0.0',port=5000,debug=True)
