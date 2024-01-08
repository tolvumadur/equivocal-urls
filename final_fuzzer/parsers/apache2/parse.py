#!/usr/bin/env python3
import os
import sys
import base64
import subprocess as sub
import traceback


HERE = os.path.dirname(os.path.realpath(__file__))


def load_url_bytes():
    assert len(sys.argv) == 2, f"Expected 1 arguments, got {len(sys.argv)-1}"
    desc = sys.argv[1]
    if desc == "testing":
        print("Putting test inputs")
        
        url_bytes = b"http://apple:sauce@example.com:80/foo/bar/baz.pdf;goo=1,2,3?height=1&you=me;so%20what#bizz?" 
        url_b64 = "aHR0cDovL2FwcGxlOnNhdWNlQGV4YW1wbGUuY29tOjgwL2Zvby9iYXIvYmF6LnBkZjtnb289MSwyLDM/aGVpZ2h0PTEmeW91PW1lO3NvJTIwd2hhdCNiaXp6Pw=="
        
        url_b64 = "aHR0cHM6Ly9uLnByN2FhLXZlcjQ1LmNvLnVrL2EvYi5jP2E9MSZiPTMsNCNmcmFn"
        url_bytes = base64.b64decode(url_b64, )
    else:
        url_b64 = input()
        url_bytes = base64.b64decode(url_b64, )
    assert type(url_bytes) is bytes
    return url_bytes, url_b64, desc

try:
    url, url_b64, desc = load_url_bytes()

    if desc == "testing":
        print("URL is:", str(url, encoding="ascii"))
        res = sub.run(["valgrind", os.path.join(HERE, "httpd-2.4.48", "httpd"), desc], capture_output=True, input=bytes(url_b64, encoding="ascii")+b"\n")
        a = res.stdout.decode(encoding="ascii", errors="backslashreplace").split("\t")
        for i, b in enumerate(a):
            if i == 0:
                continue
            print(f"{b} -- {base64.b64decode(b)}")
    else:
        res = sub.run([os.path.join(HERE, "httpd-2.4.48", "httpd"), desc], capture_output=True, input=bytes(url_b64, encoding="ascii")+b"\n")

    if res.returncode != 0 or len(res.stderr) > 0:
        if res.returncode == -11:
            sys.stderr.write(f"Error! Segfault\n")
        sys.stderr.write(str(res.stdout, encoding="utf-8", errors = "replace"))
        sys.stderr.write(f"Error ({res.returncode}) running apache-httpd parser:" + str(res.stderr, encoding="utf-8") + "\n")
        #sys.stderr.write(f"url_b64 {url_b64[-5:]}")
        exit(res.returncode)
    else:
        print(str(res.stdout, encoding="utf-8", errors="replace"))
except FileNotFoundError as err:
    sys.stderr.write(f"Unable to find apache parser: {err}")
    exit(1)
except Exception as err:
    sys.stderr.write(f"{type(err)}: {err}\n{str(traceback.format_exc())}\n")
    exit(1)



