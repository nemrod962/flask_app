from datetime import datetime
from time import sleep

from flask import Flask, Response, render_template, request

app = Flask(__name__)

index_html = """
<!doctype html><html lang=en>
<head>
    <title>SSE Stream</title>
</head>
<body>
    <h1>hello, world</h1>
    <button id="boton" onclick="sendmsg();">Gen</button>
    <input id="texto" type="text"></input>
    <ul id="events"></ul>
    <script>
    
    window.onload = function() {
        var source = new EventSource("/stream3");
        source.onmessage = function(e) {

          var newElement = document.createElement("li");
          newElement.innerHTML = e.data;

          document.getElementById("events").appendChild(newElement);
        }
    }
    

    function sendmsg()
    {
        console.log("hola buenos dias");
        var txt = document.getElementById('texto').value;
        console.log("texot: " + txt);
        var xhr = new XMLHttpRequest();
        var loc = window.location.href
        console.log('loc: ' + loc)
        loc += 'peticion'
        console.log('loc: ' + loc)
        xhr.open('POST', loc);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            //respuesta servidor
            resp = xhr.responseText;
            console.log('RESPONSE FROM SERVER: ' + resp);
        };
        xhr.send('txt='+txt);
        console.log('mensaje enviado');
    }
    </script>
</body>
</html>
"""

varGlobal = ""
varTemp = ""

@app.route('/peticion', methods=['GET','POST'])
def peticion():
    if request.method=='POST':
        var = request.form.get('txt','None')
        print "SERVER - recibido: " + var
        global varGlobal
        varGlobal = var
        return "soy /peticion"

def streamer():
    while True:
        sleep(1)
        data = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        yield 'data: {}\n\n'.format(data)

@app.route('/stream')
def stream():
    return Response(streamer(), mimetype="text/event-stream")

def streamer2():
    data = "Me has llamado a las: " + datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    print "SOY STREAMER2"
    return 'data: {}\n\n'.format(data)

@app.route('/stream2', methods=['GET','POST'])
def stream2():
    return Response(streamer2(), mimetype="text/event-stream")

def streamer3():
    global varGlobal
    global varTemp
    #varTemp = varGlobal
    while True:
        sleep(5);
        print "VAR GLOBAL: " + varGlobal
        print "VAR TEMP: " + varTemp
        if varTemp != varGlobal:
            varTemp = varGlobal
            data = "Me has llamado a las: " + datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
            return 'data: {}\n\n'.format(data)

@app.route('/stream3', methods=['GET'])
def stream3():
        return Response(streamer3(), mimetype="text/event-stream")

@app.route('/')
def index():
    return index_html

if __name__ == '__main__':
    #ssl_context sirve para utilizar https
    #la opcion adhoc indica a flask que se encargue el 
    #de crear las claves.
    #app.run(debug=True, threaded=True, ssl_context='adhoc')
    #Es necesario poner threaded=True de forma que se creen varios
    #hilos y se puedan atender peticiones.
    #Si no hay hilos, el proceso entrara en el bucle while de streamer3()
    #y dara "vueltas todo el rato" sin atender a las peticiones que le lleguen
    #del cliente.
    app.run(debug=True, threaded=True)

