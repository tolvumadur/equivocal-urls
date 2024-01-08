#!/usr/bin/env python3

from furl import furl

import sys
import base64
import traceback

PARSER_NAME = b"Python3 furl"

def report_results(Scheme, Authority, UserInfo, Hostname, Port, Path, Query, Fragment, Errors = b""):
    #list(print(type(a)) for a in [Scheme, Authority, UserInfo, Hostname, Port, Path, Query, Fragment, Errors])
    results = PARSER_NAME + b"\t" + b"\t".join(base64.b64encode(a) if type(a) is bytes else base64.b64encode(a.encode()) for a in [Scheme, Authority, UserInfo, Hostname, Port, Path, Query, Fragment]) + b"\t" + Errors + b"\n"
    print(results.decode("ascii"))

def report_failure(error):
    report_results(b"",b"",b"",b"",b"",b"",b"",b"",(error.encode("ascii", errors="backslashreplace")))


def load_url_bytes():
    assert len(sys.argv) == 2, f"Expected 1 arguments, got {len(sys.argv)-1}"
    desc = sys.argv[1]
    if desc == "testing":
        url_b64 = "TEST"
        url_bytes = b"http://apple:sauce@example.com:80/foo/bar/baz.pdf;goo=1,2,3?height=1&you=me;so%20what#bizz?" 
    else:
        url_b64 = input()
        url_bytes = base64.b64decode(url_b64, )
    assert type(url_bytes) is bytes
    return url_bytes, url_b64, desc

try:
    url, url_b64, desc = load_url_bytes()
except Exception as err:
    report_failure(f"{type(err)}: {err}\n{str(traceback.format_exc())}\n")
    exit(1)

if desc == "testing":
    print(b"URL is: "+url)

warnings = []
errors = []
testing_errors = []

try:
    parsed = furl(str(url, encoding='utf-8'))
    #print("hi")
except ValueError as err:
    report_failure(f"Parsing Error: {err}")
    exit(0)
except Exception as err:
    #if desc == "testing":
    #    sys.stderr.write(f"{len(url)}\n")
    #    sys.stderr.write(f"{type(err)}: {err}\n{str(traceback.format_exc()).replace(bar, foo)}\n")
    report_failure(f"{type(err): {err}}")
    exit(0)


report_results(
    parsed.scheme,
    parsed.netloc,
    (parsed.username if parsed.username is not None else "") + (":" + parsed.password if parsed.password is not None else ""),
    parsed.host,
    parsed.port if type(parsed.port) is bytes else str(parsed.port).encode("ascii"),
    str(parsed.path),
    str(parsed.query),
    str(parsed.fragment)
)
