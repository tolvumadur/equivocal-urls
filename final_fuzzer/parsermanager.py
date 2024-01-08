from hashlib import sha256
import base64 as b64
import random
import sys,os
from pprint import pprint
import subprocess
import json
import traceback
import concurrent.futures as pthread
from ast import literal_eval

# Where am I?
HERE = os.path.dirname(os.path.realpath(__file__))

# Get the logger
sys.path.append(os.path.join(HERE,"../logger"))
#import logger
from logger import PAINFUL, BORING, MEDIUM, HIGH

def get_parser_list(l):
    parsers = os.listdir(os.path.join(HERE, "./parsers"))
    return parsers

# Compile all the parsers or whatever they need
def prep_all_parsers(l):
    
    parser_list = get_parser_list(l)

    l.l(f"Building {len(parser_list)} test parsers.",HIGH)

    built_something = 0

    for parser_name in parser_list:
        prepper_loc = os.path.join(HERE, "./parsers", parser_name, "prep.py")
        l.l(f"Looking for a prep.py script at \n{prepper_loc}", MEDIUM)
        if not os.path.exists(prepper_loc):
            l.l(f"Could not find prepperfile for {parser_name} at: \n{prepper_loc}\nSkipping...", HIGH)
            continue
        try:
            result = subprocess.run(["python3", prepper_loc], capture_output=True)
            if result.returncode != 0:
                if "apache2" in parser_name:
                    l.l("Suppressing expected error from apache2", MEDIUM)
                    built_something += 1
                else:
                    l.l(f"Failed to prep a parser {parser_name}:\n{str(result.stderr, encoding='utf-8')}",HIGH)
                continue
            built_something += 1
            l.l(f"Built {parser_name} parser", MEDIUM)
        except Exception as err:
            l.l(f"Error building {parser_name}: {type(err)}: {err}", HIGH)

    if not built_something:
        l.l(f"Failed to build any parsers. Aborting...", HIGH)
        exit()

    return built_something

# Run a test with one parser and one URL and return the result
def test_one(msg, place):
    with open(os.path.join(HERE, ".tmp.txt"), "r") as f:
        return subprocess.run(["python3", place, msg], capture_output=True, stdin=f)

# Test in all parsers in parallel
def test_in_all(l, url, msg, outfile, cnt):

    parser_list = get_parser_list(l)

    l.l(f"Testing url in {len(parser_list)} parsers", BORING)

    tests = 0

    # Everyone will read this file
    with open(os.path.join(HERE, ".tmp.txt"),"w") as f:
        f.write(url)

    # Collect parsers
    parser_runner_paths = []
    for parser_name in parser_list:
            parser_runner_path = (os.path.join(HERE, "./parsers", parser_name, "parse.py"))
            if os.path.exists(parser_runner_path):
                parser_runner_paths.append(parser_runner_path)
            else:
                l.l(f"Could not run {parser_name} because {parser_runner_path} does not exist",HIGH)

    # Execute parsers in parallel
    results = {"URL" : url, "parsed" : []}
    try:
        with pthread.ThreadPoolExecutor(max_workers=16) as thread_pool:
            test_result_futures = {thread_pool.submit(test_one, msg, parser_runner_path): parser_runner_path.split("/")[-2] for parser_runner_path in parser_runner_paths}            
            for future_result in pthread.as_completed(test_result_futures):
                parser_name = test_result_futures[future_result]
                try:
                    result = future_result.result(timeout=60)
                    if result.returncode != 0:
                        l.l(f"Error in subprocess doing test [{parser_name}]:\n" + str(result.stderr).replace("\\n","\n"), HIGH)
                        continue
                    elif len(result.stdout) == 0:
                        l.l(f"Error in subprocess for {parser_name}, no result returned but return code was 0.\nSTDERR:\n\n{result.stderr if len(result.stderr) < 100 else result.stderr[:100]} See:\n{parser_runner_path}", HIGH)
                        continue
                    else:
                        l.l(f"Result from {parser_name} was ok", BORING)
                    tests += 1

                    a = None
                    try:
                        a = result.stdout.decode(encoding="ascii", errors="backslashreplace").split("\t")
                    except UnicodeDecodeError as err:
                        l.l(f"{parser_name} yielded an illegal output: " + str(result.stdout.split(b'\t')),HIGH)
                        l.l(f"URL was {url}", HIGH)
                        exit()

                    assert a[9].strip() not in [b"ZnJhZw==", b"I2ZyYWc=",b"ZnJhZwAA", b"ZnJhZwA="], f"{a[0]} has placed the fragment at offset 9\n{result.stdout}"
                    assert len(a) >= 10, str(a) + " " + str(len(a))

                    result = {
                    "Parser"    : a[0],
                    "Scheme"    : a[1],
                    "Authority" : a[2],
                    "UserInfo"  : a[3],
                    "Hostname"  : a[4],
                    "Port"      : a[5],
                    "Path"      : a[6],
                    "Query"     : a[7],
                    "Fragment"  : a[8],
                    "Errors"    : " ".join(a[9:])
                    }
                    #if result["Hostname"].strip() == "" and result["Errors"].replace("\n", " ").strip() == "":
                    #    print("Unexplained error")
                    #    print(a)
                    #    print(len(a))
                    #    pprint(result)
                    #    print(parser_name)
                    #    input("Press enter to get another")
                    results["parsed"].append(result)
                    l.l(f"Another URL Parsed by {tests} parsers.", BORING)
                    
                except pthread.TimeoutError as err:
                    l.l("Error in {parser_name}: Failed to parse URL within 60 seconds.", HIGH)
                    continue
                except pthread.CancelledError as err:
                    l.l("Error in {parser_name}: Future was prematurely cancelled.", HIGH)
                    continue
                except IndexError as err:
                    l.l(f"Error in {parser_name}. Malformed Output. Number of submitted fields: {len(a)}, expected at least 10", HIGH)
                    l.l(f"{a}", HIGH)



    except Exception as err:
        l.l(f"Multithreaded testing error\n{type(err)}: {err}", HIGH)
        traceback.print_exc()
        exit(1)


    assert len(results['parsed']) == len(parser_list), f"Error getting results from every parser: Expected {len(parser_list)}, got {len(results['parsed'])}"

    with open(outfile, "a") as f:
        f.write(json.dumps(results) + "\n")
        l.l(f"Written {len(results['parsed'])} to {outfile}", BORING)
    return results

