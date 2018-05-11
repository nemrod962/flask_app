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
    <ul id="events"></ul>
    <button id="boton" onclick="sendmsg();">Gen</button>
    <script>
    
    window.onload = function() {
        var source = new EventSource("/stream2");
        source.onmessage = function(e) {

          var newElement = document.createElement("li");
          newElement.innerHTML = e.data;

          document.getElementById("events").appendChild(newElement);
        }
    }
    

    function sendmsg()
    {
        console.log("hola buenos dias");
        var xhr = new XMLHttpRequest();
        var loc = window.location.href
        console.log('loc: ' + loc)
        loc += 'stream2'
        console.log('loc: ' + loc)
        xhr.open('GET', loc);
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function() {
            //respuesta servidor
            resp = xhr.responseText;
            console.log('RESPONSE FROM SERVER: ' + resp);
        };
        xhr.send('id=1');
        console.log('mensaje enviado');
    }
    </script>
</body>
</html>
"""

def streamer2():
    data = "Me has llamado a las: " + datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
    print "SOY STREAMER2"
    return 'data: {}\n\n'.format(data)

@app.route('/stream2', methods=['GET','POST'])
def stream2():
    if request.method=='GET':
        return Response(streamer2(), mimetype="text/event-stream")
    else:
        return "no"


@app.route('/')
def index():
    return index_html

if __name__ == '__main__':
    #ssl_context sirve para utilizar https
    #la opcion adhoc indica a flask que se encargue el 
    #de crear las claves.
    #app.run(debug=True, threaded=True, ssl_context='adhoc')
    app.run(debug=True)

