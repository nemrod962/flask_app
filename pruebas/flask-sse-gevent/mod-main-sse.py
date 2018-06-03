# author: oskar.blom@gmail.com
#
# Make sure your gevent version is >= 1.0
import gevent
from gevent.pywsgi import WSGIServer
from gevent.queue import Queue

from flask import Flask, Response

import time

# SSE "protocol" is described here: http://mzl.la/UPFyxY
class ServerSentEvent(object):

    def __init__(self, data):
		#texto mensaje
        self.data = data
		#~grupo. tipo de evento.
        #En el cliente, con addEventListener(),
        #podemos especificar el tipo de evento al
        #que escuchar.
        self.event = None
        #The event ID to set the EventSource object's last event ID value.
        self.id = None
        self.desc_map = {
            self.data : "data",
            self.event : "event",
            self.id : "id"
        }

    def encode(self):
        if not self.data:
            return ""
        lines = ["%s: %s" % (v, k) 
                 for k, v in self.desc_map.iteritems() if k]
        
        return "%s\n\n" % "\n".join(lines)

app = Flask(__name__)
subscriptions = []

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

@app.route("/debug")
def debug():
    return "Currently %d subscriptions" % len(subscriptions)

@app.route("/publish")
def publish():
    #Dummy data - pick up from request for real data
    def notify():
        msg = str(time.time())
        #Cada 'sub' en la lista subscriptions
        #es una instancia de gevent.queue.Queue
        for sub in subscriptions:
            sub.put(msg)
    
    gevent.spawn(notify)
    
    return "OK"

@app.route("/subscribe")
def subscribe():
    def gen():
        q = Queue()
        subscriptions.append(q)
        print "q: " + str(q)
        print "subscriptions: " + str(subscriptions)
        try:
            while True:
                #q.get() espera hasta que haya elemento en q
                #gevent.queue implementa colas sincronizadas 
                #(se comparten entre procesos).
                #CLAVE DEL FUNCIONAMIENTO. q.get() bloquea al
                #proceso hasta que la cola q contiene algun 
                #elemento.
                print "Obteniendo elemento de la cola..."
                result = q.get()
                #result = "placeholder"
                ev = ServerSentEvent("Soy subscribe: " + str(result))
                yield ev.encode()
        except GeneratorExit: # Or maybe use flask signals
            subscriptions.remove(q)

    return Response(gen(), mimetype="text/event-stream")

if __name__ == "__main__":
    app.debug = True
    server = WSGIServer(("0.0.0.0", 5000), app)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print "Terminado por el usuario"
    # Then visit http://localhost:5000 to subscribe 
    # and send messages by visiting http://localhost:5000/publish
