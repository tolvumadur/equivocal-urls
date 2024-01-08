import os
import datetime
import inspect
import re 
import random

HIGH   = 0
MEDIUM = 1
BORING = 2
PAINFUL= 3

class Logger:

    def __init__(self, verbosity, outfilename, silent):
        self.verbosity = verbosity
        self.silent = silent
        self.outfilename = outfilename
        self.outfile = open(outfilename,"w+")


    def l(self, msg, priority):
        if (priority <= self.verbosity):

            if priority == 0:
                priority_str = "HI!"
            elif priority == 1:
                priority_str = "MED"
            elif priority == 2:
                priority_str = "LOW"
            elif priority == 3:
                priority_str = "WHY"
            else:
                priority_str = "UNK"

            caller = inspect.getframeinfo(inspect.stack()[1][0])
            calling_file_name = str(caller.filename)
            calling_line_number = str(caller.lineno)

            log_msg = str(datetime.datetime.now()) + " [" + str(priority_str) +  "] " + calling_file_name + " line " + calling_line_number + " --- " + msg
            if not self.silent:
                print(log_msg)
            self.outfile.write(log_msg + os.linesep)


def parse_ABNFs(filenames, l):
    rules = {}
    for filename in filenames:
        with open(filename) as f:
            rows = f.read().split("\n")
            rows_commentless = list(";".join(row.split(";")[:-1]) if (";" in row and "\"" not in row) else row for row in rows)
            rows_stripped = list(row.strip() for row in rows_commentless)
            
            i = 0 
            while i < len(rows_stripped):
                if rows_stripped[i] == "":
                    i += 1
                    continue
                assert "=" in rows_stripped[i]
                new_rule_name = rows_stripped[i].split("=")[0].strip()
                new_rule_expansion = rows_stripped[i].split("=")[1].strip()
                while i + 1 < len(rows_stripped) and "=" not in rows_stripped[i+1]:
                    i += 1
                    if rows_stripped[i] == "":
                        continue
                    new_rule_expansion += " / ( "
                    new_rule_expansion += rows_stripped[i][1:].strip() + " )"

                if new_rule_name in rules:
                    l.l("WARNING: Rule <<<" + new_rule_name + ">>> in " + filename  + " has been overruled by a higher precedence rule!",MEDIUM)
                else:
                    rules[new_rule_name] = new_rule_expansion
                i += 1


    for rule, thing in rules.items():
        l.l(str(rule) + " = " + thing, BORING)
    return rules
        
