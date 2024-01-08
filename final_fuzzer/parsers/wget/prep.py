#!/usr/bin/env python3

import subprocess
import os
import sys


# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))


res = subprocess.run(["make", "--directory=" + os.path.join(HERE, "wget-1.21")], capture_output=True)

if (res.returncode != 0):
    sys.stderr.write(res.stderr.decode("utf-8"))
    exit(1)
else:
    exit(0)







