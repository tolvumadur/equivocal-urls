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
        url_bytes = b"https://n.praa-ver45.co.uk/a/b.c?a=1&b=3,4#frag"
        url_b64 = str(base64.b64encode(url_bytes), encoding="ascii")
        #print(url_b64)

        #url_b64 = "aHR0cHM6Ly9uLnByAWFhLXZlcjQ1LmNvLnVrL2EvYi5jP2E9MSZiPTMsNCNmcmFn"
        #url_bytes = base64.b64decode(url_b64)
        #print(url_b64)
    else:
        url_b64 = input().strip()
        url_bytes = base64.b64decode(url_b64)
    assert type(url_bytes) is bytes
    #if type(url_b64) is str:
    #    url_b64 = bytes(url_b64, encoding="ascii")
    assert type(url_b64) is str
    return url_bytes, url_b64, desc

try:
    url, url_b64, desc = load_url_bytes()

    if desc == "testing":
        print("URL is:", url)
        print("INput will be: " + str(bytes(url_b64 + "\n", encoding="ascii"))[2:-1])
        print("Input desired: " + url_b64)

    command = ["node", str(os.path.join(HERE, "parse.js")), desc]
    #res = sub.run(command, capture_output=True, input=bytes(url_b64, encoding="ascii")+b"\n")
    res = sub.run(command, capture_output=True, input=bytes(url_b64, encoding="ascii") )#bytes(url_b64, encoding="ascii")+b"\n")
    #sys.stdout.write(" ". join(command) + "\n")


    if res.returncode != 0 or len(res.stderr) > 0:
        #sys.stderr.write(str(res.stdout, encoding="utf-8", errors = "replace"))
        sys.stderr.write(f"Error ({res.returncode}) running NodeJS parser:\n" + str(res.stderr, encoding="utf-8") + "\n")
        #sys.stderr.write(f"url_b64 {url_b64[-5:]}")
        exit(res.returncode)
    else:
        print(str(res.stdout, encoding="utf-8", errors="replace"))

except Exception as err:
    sys.stderr.write(f"{type(err)}: {err}\n{str(traceback.format_exc())}\n")
    exit(1)



