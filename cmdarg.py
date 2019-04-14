#!/usr/bin/env python

# Simple python command line args processor

import sys

class NotEnoughArgs(Exception):
    pass
class TooManyArgs(Exception):
    pass

def get_arg_dict(minargs=-1,maxargs=-1):
    args = {0:sys.argv[0]}
    arglength = len(sys.argv)
    count = 1
    paramless = 1
    while count < arglength:
        arg = sys.argv[count]
        count += 1
        if arg[0] == "-":
            if "=" in arg:
                data = arg.split("=")
                args[data[0].strip("-")] = data[1]
            elif count==arglength or sys.argv[count][0] == "-":
                args[arg.strip("-")] = None
            else:
                args[arg.strip("-")] = sys.argv[count]
                count += 1
        else:
            args[paramless] = arg
            paramless += 1
    if paramless-1 < minargs:
        raise NotEnoughArgs
    if paramless-1 > maxargs and maxargs!=-1:
        raise TooManyArgs
    return args

if __name__ == "__main__":
    print get_arg_dict()
