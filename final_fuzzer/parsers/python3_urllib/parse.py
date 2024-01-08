#! /usr/bin/env python3

from urllib.parse import urlparse
import sys
import base64


PARSER_NAME = b"Python3 urllib.urlparse"

def report_results(Scheme, Authority, UserInfo, Hostname, Port, Path, Query, Fragment, Errors = b""):
    results = PARSER_NAME + b"\t" + b"\t".join(base64.b64encode(a) for a in [Scheme, Authority, UserInfo, Hostname, Port, Path, Query, Fragment]) + b"\t" + Errors
    print(results.decode("ascii", errors="backslashreplace"))

def report_failure(error):
    report_results(b"",b"",b"",b"",b"",b"",b"",b"",error.encode("ascii"))

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

parsed = urlparse(b"")

try:
    url, url_b64, desc = load_url_bytes()
except Exception as err:
    report_failure(f"{type(err)}: {err}")
    exit(1)
try:
    parsed = urlparse(url)
    
    #Force lazy loading
    parsed.port

    path = parsed.path if parsed.path is not None else b""

    if parsed.params != b"":
        path += b";" + parsed.params 
    
except Exception as err:
    report_failure(f"{type(err)}: {err}")
    exit()

if desc == "testing":
    print(url)
    print(parsed)

report_results(
    parsed.scheme    if parsed.scheme is not None else b"",
    parsed.netloc    if parsed.netloc is not None else b"",
    (parsed.username if parsed.username is not None else b"") + (b":" + parsed.password if parsed.password is not None else b""),
    parsed.hostname  if parsed.hostname is not None else b"",
    parsed.port      if type(parsed.port) is bytes else str(parsed.port).encode("ascii"),
    path,
    parsed.query     if parsed.query is not None else b"",
    parsed.fragment  if parsed.fragment is not None else b""
)
