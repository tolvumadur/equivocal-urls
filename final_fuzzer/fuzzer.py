#!/usr/bin/env python3

import os
import sys
import base64 as b64
import argparse as ap
import math

# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))

# Get the logger
sys.path.append(os.path.join(HERE, "..", "logger"))
import logger
from logger import PAINFUL, BORING, MEDIUM, HIGH

import unicode

import parsermanager as pm
import test as t

# Arguments
argparser = ap.ArgumentParser(description= "Fuzz generated URLs")
argparser.add_argument("--verbosity",   "-v", default=0, type=int,                          help="Set verbosity 0-2. 0 is default.")
argparser.add_argument("--silent",      "-s,", action="store_true",                            help="Print nothing to stdout. Only log.")
argparser.add_argument("--logfile",     "-l", default=os.path.join(HERE,"3_fuzzer.log"), type=str,help="Path to write log. Appends.")
argparser.add_argument("--version",     "-V", action="store_true",                             help="Print version and exit.")
argparser.add_argument("--urldir",     "-u", default=os.path.join(HERE, "..", "url_gen", "out"), type=str,    help="generated URL directory.")
argparser.add_argument("--outfile",     "-o", default=os.path.join(HERE,"out"), type=str,    help="output directory")

#Parse command line arguments
args = argparser.parse_args()

# Initialize Logger
version = "URL Fuzzer 3 -- Trying everything in a hostname"
l = logger.Logger(args.verbosity, args.logfile, args.silent)

l.l("Prepping all parsers", HIGH)

n_containers = pm.prep_all_parsers(l)

l.l(f"Built {n_containers} parsers", HIGH)

if n_containers == 0:
    l.l(f"Could not start any parsers. Aborting...", HIGH)
    exit()

outfile = args.outfile
cnt = 0

bp = {
    "length" : 1,
    "byteorder" : "big",
    "signed" : False 
}

#Every 1 byte  0.26K
one_byte_outfile = os.path.join(HERE,    "data", "one_byte.json")

#Every 2 bytes 65.6K
two_bytes_outfile = os.path.join(HERE,   "data", "two_bytes.json")

#Every 1 utf-8 38K
one_unicode_outfile = os.path.join(HERE, "data", "unicode.json")

#TODO how many skips in each?
# read the row counts, ignore blank line
skip1 = 0
skip2 = 0
skip3 = 0

try:
    with open(one_byte_outfile, "r+") as f:
        skip1 = len(f.readlines())
        if skip1 > 0:
            l.l(f"on dataset 1 we can skip {skip1}",HIGH)
except:
    pass

try:
    with open(two_bytes_outfile, "r+") as f:
        skip2 = len(f.readlines())
        if skip2 > 0:
            l.l(f"on dataset 2 we can skip {skip2}",HIGH)
except:
    pass

try:
    with open(one_unicode_outfile, "r+") as f:
        skip3 = len(f.readlines())
        if skip3 > 0:
            l.l(f"on dataset 3 we can skip {skip3}",HIGH)
except:
    pass

l.l("Testing dataset 1 with one byte", HIGH)

# every one byte
done = 0
skipped = 0
for i in range(256):
        if skip1 != 0 and skip1 == i:
            l.l(f"Skipping {i} already done from one-byte", HIGH)
        if skipped < skip1:
            skipped += 1
            continue
        done += 1
        fuzz = i.to_bytes(1,byteorder="big")
        url = b"https://n.pr" + fuzz  + b"aa-ver45.co.uk/a/b.c?a=1&b=3,4#frag"
        url_b64 = str(b64.b64encode(url), encoding="ascii")
        t.test(l, url_b64, b"", one_byte_outfile, cnt)
l.l(f"skipped {skipped} + did {done} = {skipped + done} of 256",HIGH)
assert skipped + done == 256, "uh-oh"
assert skip1 + done == 256, f"uh-oh {skip1 + done}"

l.l("Testing dataset 2 with two bytes", HIGH)
done = 0
skipped = 0

# every two bytes
for i in range(256):
    for j in range(256):

        iteration = i*(2**8) + j + 1

        #print(iteration)

        if skip2 > 0 and skip2 == iteration:
            l.l(f"Skipping {skip2} already done from two-byte", HIGH)

        if skipped < skip2:
            skipped += 1
            continue
        elif skipped == skip2:
            f"We've skipped {skip2} already done from two-byte."

        assert skipped == skip2, f"skipped too many! skipped {skipped} skip2 was only {skip2}"

        if iteration % 1000 == 0:
            l.l(f"Parsed {iteration} from this group!",HIGH)

        done += 1
        fuzz = i.to_bytes(1,byteorder="big") + j.to_bytes(1,byteorder="big")  #chr(i) + chr(j)
        url = b"https://n.pr" + fuzz + b"aa-ver45.co.uk/a/b.c?a=1&b=3,4#frag"
        url_b64 = str(b64.b64encode(url), encoding="ascii")
        t.test(l, url_b64, b"", two_bytes_outfile, cnt)

l.l(f"skipped {skipped} + did {done} = {skipped + done} of {256*256}",HIGH)

assert skipped + done == 256**2, "uh-oh"
assert skip2 + done == 256**2, "uh-oh"

l.l("Testing dataset 3 with unicode over 2 bytes", HIGH)

# every unicode (longer than two bytes)
skipped = 0
tst = 0
skip_redundant = 0
for i in unicode.get_all_valid_unicode_points():
    #try:
    fuzz = i#chr(i).encode('utf-8', 'error')
        #assert fuzz == i, f"{hex(i)} is what we wanted, but we got {hex(int.from_bytes(fuzz, byteorder='big', signed=False))}"
    #except LookupError as err:
        #print(f"There was a problem with {hex(i)}")
    #    bc = math.ceil(len(hex(i)[2:])/2)
    #    fuzz = i.to_bytes(bc,byteorder="big", signed=False)
        #print(fuzz)
        #exit(1)
    if len(fuzz) <= 2:
        #Skip things that were already in 1 or 2 byte land
        skip_redundant += 1
        continue
    if skip3 != 0 and skip3 == done:
        l.l(f"Skipping {i} already done from unicode", HIGH)
    if skipped < skip3:#THIS STILL HAS BUG
        skipped += 1
        continue
    url = b"https://n.pr" + fuzz  + b"aa-ver45.co.uk/a/b.c?a=1&b=3,4#frag"
    url_b64 = str(b64.b64encode(url), encoding="ascii")
    tst += 1
    if tst % 1000 == 0:
        print(f"Done {tst} this session")
    t.test(l, url_b64, b"", one_unicode_outfile, cnt)
l.l(f"skipped {skipped} + did {tst} + redundant skips {skip_redundant} = {skipped + tst + skip_redundant} of {len(list(unicode.get_all_valid_unicode_points()))}",HIGH)
assert skipped + tst + skip_redundant == len(list(unicode.get_all_valid_unicode_points())), "uh-oh"

l.l(f"Done. Tested {cnt} URLs", HIGH)
