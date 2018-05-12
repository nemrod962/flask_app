# -*- coding: UTF-8 -*-
from gevent.pywsgi import WSGIServer

from flask import Flask, Response, request

import time

from sse_handler import SSEHandler


app = Flask(__name__)
#subscriptions = []
sseHand = SSEHandler()

# Client code consumes like this.
@app.route("/")
def index():
    debug_template = """
     <html>
       <head>
       </head>
       <body>
         <h1>Server sent events</h1>
         <div id="event"></div>
         <script type="text/javascript">

         var eventOutputContainer = document.getElementById("event");
         var evtSrc = new EventSource("/subscribe");

         evtSrc.onmessage = function(e) {
             console.log(e.data);
             eventOutputContainer.innerHTML = e.data;
         };

         </script>
       </body>
     </html>
    """
    return(debug_template)

@app.route("/aux")
def indexAux():
    debug_template = """
     <html>
       <head>
       <script src="//ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>
       </head>
       <body>
         <h1>Server sent events</h1>
         <div>This is another page</div>
         <input id="texto" type="text"></input>
         <button id="boton" onclick="sendSSE2();">Enviar mensaje</button>
         <div id="event"></div>
         <script type="text/javascript">
    
         function sendSSE()
         {
            var msg = document.getElementById('texto').value
            console.log("texto: " + msg);
			var xhr = new XMLHttpRequest();
			var loc = window.location.origin
			console.log('loc: ' + loc)
			loc += '/publish'
            //loc = 'http://0.0.0.0:5000/publish'
			console.log('loc: ' + loc)
			xhr.open('POST', loc);
			xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
			xhr.onload = function() {
				//respuesta servidor
				resp = xhr.responseText;
				console.log('RESPONSE FROM SERVER: ' + resp);
			};
			xhr.send('txt='+msg);
			console.log('mensaje enviado');
         }

         //same but with jQuery. Uses POST.
         function sendSSE2()
         {
            var url = window.location.origin + '/publish';
            var msg = document.getElementById('texto').value;
            $.post(url, 'txt='+msg, function(e)
                {
                    console.log('sendSSE2() . resp. server: ' + e)
                }
            );
         }

         //same but with jQuery. Uses GET.
         function sendSSE3()
         {
            var url = window.location.origin + '/publish';
            var msg = document.getElementById('texto').value;
            var finalURL = url+'?txt='+msg
            $.get(finalURL, function(e)
                {
                    console.log('sendSSE3() . resp. server: ' + e)
                }
            );
         }

         var eventOutputContainer = document.getElementById("event");
         var evtSrc = new EventSource("/subscribe");

         evtSrc.onmessage = function(e) {
             console.log(e.data);
             eventOutputContainer.innerHTML = e.data;
         };

         </script>
       </body>
     </html>
    """
    return(debug_template)

@app.route("/debug")
def debug():
    #return "Currently %d subscriptions" % len(SSEHandler.listaSuscripciones)
    return "Currently %d subscriptions" % len(sseHand.listaSuscripciones)

@app.route("/publish", methods=['GET','POST'])
def publish():
    if request.method=='POST':
        msg = request.form.get("txt")
        print "args: " + str(request.args)
        print "data: " + str(request.data)
        print "form: " + str(request.form)
        print "values: " + str(request.values)
        print "TEXTO: " + str(msg)
        return sseHand.createSSE(msg)
    elif request.method=='GET':
        msg = request.args.get("txt")
        print "args: " + str(request.args)
        print "data: " + str(request.data)
        print "form: " + str(request.form)
        print "values: " + str(request.values)
        print "TEXTO: " + str(msg)
        return sseHand.createSSE(msg)
    return sseHand.createSSE()

@app.route("/subscribe")
def subscribe():
    return sseHand.sendSSE()

if __name__ == "__main__":
    app.debug = True
    #IMPORTANTE. ES NECESARIO EMPLEAR WGSISserver de gevent
    #para lanzar la aplicación.
    #Al emplear SSE, vamos a necesitar un proceso que se encargue
    #de estar trabajando con la cola de SSEs todo el tiempo.
    #SI no ejecutamos la aplicación mediante varios procesos (usando
    #gevent.WGSIServer), el único proceso de la aplicación se quedará 
    #trabajando con esta cola de SSE y no podrá atender al cliente.
    server = WSGIServer(("0.0.0.0", 5000), app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "Terminado por el usuario"
    # Then visit http://localhost:5000 to subscribe 
    # and send messages by visiting http://localhost:5000/publish
