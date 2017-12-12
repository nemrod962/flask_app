#include beebotte SDK for python
from beebotte import *

#bclient = BBT("API_KEY", "SECRET_KEY")
_accesskey = "6dcd5477c26e32e1819f487f169f2a45"
_secretkey = "e6912a135c4da71e9b2d605046f534be154d06f32ac5784f53a562ccb48d336b"
_hostname = "api.beebotte.com"
bclient = BBT(_accesskey, _secretkey, hostname = _hostname)

#create channel

try:
    bclient.addChannel(
        "dev",
        label = "channel label",
        description = "channel description",
        ispublic = True,
        resources = [{
            "name": "res1",
            "vtype": BBT_Types.String
        }, 
        {
            "name": "res2",
            "label": "resource 2",
            "vtype": BBT_Types.String
        }, 
        {
            "name": "res3",
            "description": "resource 3 description",
            "vtype": BBT_Types.Number,
            "sendOnSubscribe": True
        }
        ]
    )
except:
    print "Error when creating channel \"dev\""

#WRITE DATA

#Create a Resource object
res1 = Resource(bclient, 'dev', 'res1')
#write to the resource
res1.write('Hello World')

#Array of messages
bclient.writeBulk('dev', [
        {"resource": "res1", "data": "Good World"},
        {"resource": "res2", "data": "Bye"}
])

#READ DATA
#read resources
records1 = bclient.read('dev', 'res1', limit = 5)
print "Estoy leyendo.\n records1: "
for x in records1:
    print x
#read resource statistics
records2 = bclient.read('dev', 'res1', limit = 24, source = 'hour-stats')
print "Estoy leyendo.\n records2: "
for x in records2:
    print x
