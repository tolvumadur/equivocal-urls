#!/usr/bin/env python3

import subprocess
import os
import sys

# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))

try:
    res = subprocess.run(["gcc", "-g", os.path.join(HERE, "main.c"), "-lcurl", "-o", os.path.join(HERE, "curl")], capture_output=True)
except Exception as err:
    sys.stderr.write("Error running gcc command: " + str(err))
    exit(2)

if (res.returncode == 1):
    sys.stderr.write(f"Return code was {res.returncode}.\n" + str(res.stderr, encoding="utf-8"))
    exit(1)

else:
    exit(0)







