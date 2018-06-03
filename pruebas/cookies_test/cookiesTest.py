from flask import Flask, url_for, request, render_template, redirect, make_response
import datetime as dt
app = Flask(__name__) 


@app.route('/')
def index():
   return render_template('index.html')

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
       user = request.form['userIdText']
       print "USARIO: " + str(user) 
   
   resp = make_response(render_template('readcookie.html'))
   #resp = make_response(render_template('readcookie.html'))
   #Tiempo caducidad de la cookie
   lapso = dt.timedelta(seconds=20)
   cadTime=dt.datetime.now() + lapso
   print "LAPSO: " + str(lapso)
   print "TIEMPO ACTUAL: " + str(dt.datetime.now())
   print "CADUCA EN : " + str(cadTime)
   resp.set_cookie('cookieName', user, expires=cadTime)
   resp.set_cookie('animal', 'oveja', expires=cadTime)
   
   return resp
"""
@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('cookieName')
   return '<h1>welcome '+str(name)+'</h1>'
"""
#@app.route('/test')
@app.route('/getcookie')
def testaso():
    name = request.cookies.get('cookieName')
    asd = request.cookies.get('animal')
    print "DEBUG: Cookie - " + str(request.cookies)

    return '<h1>hola? '+str(name)+\
    '<br>'+ 'Eres un(a) ' + str(asd) +"<br>"+\
    "borrar? - <a href='/delcookie'>click</a> </h1>"

@app.route('/delcookie')
def borrado():
    cokkie=request.cookies
    resp=make_response("cookies borradas<br><a href='/getcookie'>Link</a>")
    for key in cokkie:
        resp.set_cookie(key,'',expires=0)

    return resp

if __name__ == "__main__":
    app.run(host='0.0.0.0', port='5000')

