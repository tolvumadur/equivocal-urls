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
        #url_b64 = "TEST"
        
        url_bytes = b"http://apple:sauce@example.com:80/foo/bar/baz.pdf;goo=1,2,3?height=1&you=me;so%20what#bizz?" 
        #url_bytes = b"https://n.pr\\abc@e.gg" 
        url_b64 = base64.b64encode(url_bytes).decode("ascii")
    else:
        url_b64 = input()
        url_bytes = base64.b64decode(url_b64, )
    assert type(url_bytes) is bytes
    return url_bytes, url_b64, desc

try:
    url, url_b64, desc = load_url_bytes()

    if desc == "testing":
        print("URL is:", str(url, encoding="ascii"))
        print(f"URL encoded, that is {bytes(url_b64, encoding='ascii')} : {base64.b64decode(url_b64)}")
        #desc = "Test Input from Python"

    res = sub.run([os.path.join(HERE, "curl"), desc], capture_output=True, input=bytes(url_b64, encoding="ascii")+b"\n")

    if res.returncode != 0 or len(res.stderr) > 0:
        #sys.stderr.write(str(res.stdout, encoding="utf-8", errors = "replace"))
        sys.stderr.write(f"Error ({res.returncode}) running libcurl parser:\n" + str(res.stderr))
        sys.stderr.write(f"\nstdout: {str(res.stdout)}\n")
        exit(res.returncode)
    else:
        print(str(res.stdout, encoding="utf-8", errors="replace"))
        if sys.argv[1] == "testing":
            for i in str(res.stdout, encoding="utf-8", errors="replace").split("\t")[1:]:
                print(str(base64.b64decode(i), encoding="utf-8", errors="backslashreplace"))

except FileNotFoundError as err:
    sys.stderr.write("compiled version of libcurl not found.")
    exit(2)
except Exception as err:
    sys.stderr.write(f"{type(err)}: {err}\n{str(traceback.format_exc())}\n")
    exit(1)



