import base64 as b64
import sys,os


# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))

import parsermanager as pm

# Get the logger
sys.path.append(os.path.join(HERE,"../logger"))
import logger
from logger import PAINFUL, BORING, MEDIUM, HIGH

def test(l, url_b64, msg, outfile, cnt):
    
    url = b64.b64decode(url_b64)
    
    l.l(f"Testing url: {msg}\n{url[:100] if len(url) > 100 else url}",BORING)

    pm.test_in_all(l, url_b64, msg, outfile, cnt)

    l.l(f"This URL done testing: {msg}\n{url[:100] if len(url) > 100 else url}",BORING)
