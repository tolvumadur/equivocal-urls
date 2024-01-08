#!/usr/bin/env python3

import subprocess
import os
import sys


# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))


res = subprocess.run(["make", "--directory=" + os.path.join(HERE, "httpd-2.4.48")], capture_output=True)

if (res.returncode != 0):
    sys.stderr.write(str(res.stderr))
    exit(1)

else:
    print(str(res.stdout.replace(b"-I", b"\n-I"),encoding="utf-8"))
    print(str(res.stderr, encoding="utf-8"))
    exit(0)







