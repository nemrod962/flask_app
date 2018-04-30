# -*- coding: UTF-8 -*-

from flask import Flask, url_for, request, render_template, redirect, make_response
import datetime as dt

app = Flask(__name__) 

#Añade atributo a la funcion, el 
#cual indica que se le excluda de 
#la comprobacion
def exclude_from_checking(func):
    func._exclude_from_checking = True
    return func

#Indico funciona ejecutar antes de requests
@app.before_request
def check_cookies(*args, **kwargs):
    #default value.
    #Indica si hay que ejecutar el checkeo o no
    run_check=True

    #You can handle 404s difeerently here if u want.
    #request.endpoint es la peticion al servidor
    #app.view_functions contiene todas las view functions 
    #definidas en la app.
    #
    #Si se cumple este if, significa que la ruta pedida por el cliente
    #es correcta y hay una view funciton asociada a ella
    if request.endpoint in app.view_functions:
        #Obtengo en view_func la funcion que se tiene que ejecutar
        #al acceder a la ruta que ha pedido el cliente.
        #Si por ejemlo se ha pedido la ruta '/', en view_func
        #tendremos al funcion index().
        view_func = app.view_functions[request.endpoint]
        run_check= not hasattr(view_func, '_exclude_from_checking')
    print 'Checkear cookies en {0}: {1}'.format(request.path, run_check)

@app.route('/')
@exclude_from_checking
def index():
   return render_template('index.html')

@app.route('/setcookie', methods = ['POST', 'GET'])
def setcookie():
   if request.method == 'POST':
       user = request.form['userIdText']
       print "USARIO: " + str(user) 
   
   resp = make_response(render_template('readcookie.html'))
   resp.set_cookie('cookieName', user)
   resp.set_cookie('animal', 'oveja')
   
   return resp

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

