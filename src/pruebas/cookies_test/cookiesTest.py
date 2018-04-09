from flask import Flask, url_for, request, render_template, redirect, make_response
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
   resp.set_cookie('cookieName', user)
   
   return resp

@app.route('/getcookie')
def getcookie():
   name = request.cookies.get('cookieName')
   return '<h1>welcome '+str(name)+'</h1>'
@app.route('/test')
def testaso():
   name = request.cookies.get('cookieName')
   return '<h1>hola? '+str(name)+'</h1>'


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='3000')

