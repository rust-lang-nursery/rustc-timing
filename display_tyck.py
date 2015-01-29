# Displays info about type checking time

import json
import os
import sys


def display(date):
    in_name = os.path.join('processed', date + '.json')

    with open(in_name) as in_file:
        display_data(json.load(in_file))


def display_data(data):
    for crate in data['times']:
        print "crate:", crate['crate']
        print "total time:", crate['total']
        tyck = crate['times']['type checking']
        if not tyck:
            print "no times for type checking"
            continue
        print "time in type checking: %.3f (%.1f%%; %.2f)"%(tyck['time'], tyck['percent'], tyck['ratio_llvm'])
        print



if len(sys.argv) <= 1:
    print "Requires filename of data as an argument"
    exit(1)

display(sys.argv[1])

