# Displays totals for each phase across all crates

import json
import os
import sys


def display(date):
    in_name = os.path.join('processed', date + '.json')

    with open(in_name) as in_file:
        display_totals(json.load(in_file))

def accumulate(dic, key, value):
    if key not in dic:
        dic[key] = 0.0

    dic[key] += value

def display_totals(data):
    totals = {}
    for crate in data['times']:
        accumulate(totals, 'total', crate['total'])
        for k in crate['times'].keys():
            accumulate(totals, k, crate['times'][k]['time'])

    totals = totals.iteritems()

    # Sort by time, largest first
    totals = sorted(totals, key = lambda (k, v): v, reverse=True)

    for (k, v) in totals:
        if v >= 0.01:
            print k + ':', v


if len(sys.argv) <= 1:
    print "Requires filename of data as an argument"
    exit(1)

display(sys.argv[1])

