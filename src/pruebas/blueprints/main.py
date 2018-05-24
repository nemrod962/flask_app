"""
DIFERENTES PRUEBAS CON FLASK
"""
from flask import Flask, url_for, request, render_template, redirect
#blueprints
from views.blue1 import vista1
from views.blue2 import vista2

numero = 0

app = Flask(__name__) 
app.register_blueprint(vista1)
app.register_blueprint(vista2)

#Functions for different routes in the server
"""
@app.route("/") 
def test():
    return render_template("template.html")
"""

@app.route("/map")
def site_map():
	import urllib
	output = []
	for rule in app.url_map.iter_rules():
		options = {}
		for arg in rule.arguments:
			options[arg] = "[{0}]".format(arg)

		methods = ','.join(rule.methods)
		url = url_for(rule.endpoint, **options)
		line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
		output.append(line)

	for line in sorted(output):
		print line
	return str(output)

#LAUNCH APP
if __name__ == "__main__":
    app.run(host='0.0.0.0',port=5000)


