#!/usr/bin/env python3

import subprocess
import os
import sys


# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))


res = subprocess.run(["javac", os.path.join(HERE, "Parse.java")], capture_output=True)

if (res.returncode != 0):
    sys.stderr.write(str(res.stderr, encoding="utf-8") + str(res.stdout, encoding="utf-8"))
    exit(res.returncode)

else:
    exit(0)







