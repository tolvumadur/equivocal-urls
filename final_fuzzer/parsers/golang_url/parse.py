#!/usr/bin/env python3

import os
import sys
import base64
import subprocess as sub
import traceback

# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))


def load_url_bytes():
    assert len(sys.argv) == 2, f"Expected 1 arguments, got {len(sys.argv)-1}"
    desc = sys.argv[1]
    if desc == "testing":
        #url_b64 = "TEST"
        
        url_bytes = b"http://apple:sauce@example.com:80/foo/bar/baz.pdf;goo=1,2,3?height=1&you=me;so%20what#bizz?" 
        url_b64 = "aHR0cDovL2FwcGxlOnNhdWNlQGV4YW1wbGUuY29tOjgwL2Zvby9iYXIvYmF6LnBkZjtnb289MSwyLDM/aGVpZ2h0PTEmeW91PW1lO3NvJTIwd2hhdCNiaXp6Pw=="
    else:
        url_b64 = input()
        url_bytes = base64.b64decode(url_b64, )
    assert type(url_bytes) is bytes
    return url_bytes, url_b64, desc

try:
    url, url_b64, desc = load_url_bytes()

    if desc == "testing":
        print("URL is:", str(url, encoding="ascii"))

    res = sub.run(["go", "run", str(os.path.join(HERE, "main.go")), desc], capture_output=True, input=bytes(url_b64, encoding="ascii")+b"\n")

    if res.returncode != 0 or len(res.stderr) > 0:
        sys.stderr.write("Error running go parser:"+ str(res.stderr))
    else:
        print(str(res.stdout, encoding="utf-8", errors="backslashreplace"))

except Exception as err:
    sys.stderr.write(f"{type(err)}: {err}\n{str(traceback.format_exc())}\n")
    exit(1)



