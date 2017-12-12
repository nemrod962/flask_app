#!/bin/sh
#host -> 	172.16.199.1
#vm -> 		172.16.199.128
#cat $1 | nc -l -p 1234
tar -ac ./myfiles -f myflask.tar
cat myflask.tar | nc -l -p 1234
rm myflask.tar
