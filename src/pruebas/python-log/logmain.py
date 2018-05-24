import logging
import sys

from aux import suma

logfile="python.log"
formato = '%(asctime)s - %(levelname)s - %(message)s'
#limpio archivo log
logging.FileHandler(logfile, mode='w')
logging.basicConfig(filename=logfile, format=formato)
log = logging.getLogger()
log.setLevel(logging.DEBUG)

ch=logging.StreamHandler(sys.stdout)
ch.setLevel(logging.WARNING)
formatter = logging.Formatter(formato)
ch.setFormatter(formatter)
log.addHandler(ch)

def msg(men):
    logging.info(men)
def alert(men):
    logging.warning(men)

suma(1,2)
