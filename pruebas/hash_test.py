# -*- coding: utf-8 -*-
#Ejemplo de hashes para contraseñas
#wekzeug emplea SHA1, lo cual no es muy seguro.
#Es mejor emplear passlib
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

print("-------------------------------------------------------")

from passlib.hash import pbkdf2_sha256
#salt_size puede no ser especificado. Por defecto es 16
#hash3 = pbkdf2_sha256.encrypt("password", rounds=200000, salt_size=16)
hash3 = pbkdf2_sha256.hash("password")
print "pbkdf2_sha256.verify(foobar, hash)"
print pbkdf2_sha256.verify("foobar", hash3)
print "pbkdf2_sha256.verify(password, hash)"
print pbkdf2_sha256.verify("password", hash3)

