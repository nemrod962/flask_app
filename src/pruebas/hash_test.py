# -*- coding: utf-8 -*-
#Ejemplo de hashes para contraseñas
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
hash1 = generate_password_hash('foobar')
print "hash1 -> foobar:" + str(hash1)
hash2 = generate_password_hash('foobar')
print "hash2 -> foobar:" + str(hash2)
#son diferentes (usan sal?), pero podemos comprabar del siguiente modo
res1 = check_password_hash(hash1, 'foo')
print "check_password_hash(hash1, 'foo') : " + str(res1)
res2 = check_password_hash(hash1, 'foobar')
print "check_password_hash(hash1, 'foobar') : " + str(res2)
res3 = check_password_hash(hash2, 'foobar')
print "check_password_hash(hash2, 'foobar') : " + str(res3)

