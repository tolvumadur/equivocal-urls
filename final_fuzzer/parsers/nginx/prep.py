#!/usr/bin/env python3

import subprocess
import os
import sys


# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))


res = subprocess.run(["make", "--directory=" + os.path.join(HERE, "nginx1-20-stable")], capture_output=True)

if (res.returncode == 1):
    sys.stderr.write(res.stderr)
    exit(1)

else:
    #print(str(res.stdout.replace(b"-I", b"\n-I"),encoding="utf-8"))
    print(str(res.stderr, encoding="utf-8"))
    exit(0)







