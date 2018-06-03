#!/bin/bash
BORRAR=('*.pyc' 'ghostdriver.log' 'screen.png' 'log.txt')
for ENTRY in ${BORRAR[*]}
do
    find ../src -name $ENTRY -exec echo "borrar {}" \;
    find ../src -name $ENTRY -exec rm {} \;
done
