from datetime import datetime
from time import sleep

from flask import Flask, Response, render_template

app = Flask(__name__)

index_html = """
<!doctype html><html lang=en>
<head>
    <title>SSL Stream</title>
</head>
<body>
    <h1>hello, world</h1>
    <ul id="events"></ul>
    <script>
    window.onload = function() {
        var source = new EventSource("/stream");
        source.onmessage = function(e) {

          var newElement = document.createElement("li");
          newElement.innerHTML = e.data;

          document.getElementById("events").appendChild(newElement);
        }
    }
    </script>
</body>
</html>
"""

def streamer():
    while True:
        sleep(1)
        data = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
        yield 'data: {}\n\n'.format(data)

@app.route('/stream')
def stream():
    return Response(streamer(), mimetype="text/event-stream")

@app.route('/')
def index():
    return index_html

if __name__ == '__main__':
    #ssl_context sirve para utilizar https
    #la opcion adhoc indica a flask que se encargue el 
    #de crear las claves.
    app.run(debug=True, threaded=True, ssl_context='adhoc')
    #app.run(debug=True, threaded=True)

