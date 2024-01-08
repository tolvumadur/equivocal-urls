#!/usr/bin/env python3
import random as r
from stat import UF_COMPRESSED
import sys,os
import json

#https://www.unicode.org/Public/UCD/latest/ucd/UnicodeData.txt

# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(HERE, "codepoints.csv"), "r") as f:
    unicode = list(((a.strip()) if a != "" else 0 for a in f.read().split('\n')))
    unicode.remove(0)


def get_all_valid_unicode_points():
    if "ucp" in locals():
        return ucp
    else:
        ucp = []
        for a in unicode:
            try:
                ucp.append(chr(int(a, 16)).encode(encoding="UTF-8"))
            except UnicodeEncodeError as err:# UnicodeEncodeError as err:
                b = chr(int(a, 16)).encode(encoding="UTF-8", errors="surrogatepass")
                ucp.append(b)
                #print (ucp[-1])
                #exit(1)
        return ucp


def get_random_unicode_point():
    return r.choice(get_all_valid_unicode_points())



ucp = get_all_valid_unicode_points()

if __name__ == "__main__":
    print("This is the Unicode Getter")

    a = get_random_unicode_point()
    print(a)
