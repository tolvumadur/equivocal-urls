#! /usr/bin/env python3


from ast import literal_eval as le
from rfc import URLParsingException, urlparse, galump
import time
from timeit import default_timer as timer
from traceback import print_exc as backtrace

import sys
import base64
from hashlib import sha256

PARSER_NAME = b"rfc3986"

def report_results(Scheme, Authority, UserInfo, Hostname, Port, Path, Query, Fragment, Errors = b""):
    #list(print(type(a)) for a in [PARSER_NAME, Scheme, Authority, UserInfo, Hostname, Port, Path, Query, Fragment, Errors])
    results = PARSER_NAME + b"\t" + b"\t".join(base64.b64encode(a) for a in [Scheme, Authority, UserInfo, Hostname, Port, Path, Query, Fragment]) + b"\t" + Errors   
    print(results.decode("ascii", errors="backslashreplace"))

def report_failure(error):
    if type(error) is str:
        report_results(b"",b"",b"",b"",b"",b"",b"",b"",error.encode())
    elif type(error) is bytes:
        report_results(b"",b"",b"",b"",b"",b"",b"",b"",error)
    else:
        report_results(b"",b"",b"",b"",b"",b"",b"",b"",b"Error Recording Error")

def load_url_bytes():
    assert len(sys.argv) == 2, f"Expected 1 arguments, got {len(sys.argv)-1}"
    desc = sys.argv[1]
    if desc == "testing":
        url_b64 = "TEST"
        url_bytes = b"http://apple:sauce@example.com:80/foo/bar/baz.pdf;goo=1,2,3?height=1&you=me;so%20what#bizz?\n" 
        url_bytes = b"https://n.prZZaa-ver45.co.uk/a/b.c?a=1&b=3,4#frag\n" 
    else:
        url_b64 = input()
        url_bytes = base64.b64decode(url_b64, )
    assert type(url_bytes) is bytes
    return url_bytes.strip(), url_b64, desc

try:
    url, url_b64, desc = load_url_bytes()
except Exception as err:
    report_failure(f"{type(err)}: {err}")
    exit(0)

try:
    parsed = urlparse(url)
except URLParsingException as err:
    report_failure(f"Error parsing URL: {err}")
    exit()
except Exception as err:
    report_failure(f"Internal Parser Error: {type(err)}: {err}")
    backtrace()
    exit(1)

report_results(
    parsed.scheme,
    parsed.authority,
    parsed.userinfo,
    parsed.hostname,
    parsed.port if type(parsed.port) is bytes else str(parsed.port).encode("ascii"),
    parsed.path,
    parsed.query,
    parsed.fragment
)

