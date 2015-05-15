import json
import os
import re
import sys

VERBOSE = False

re_commit = re.compile("commit (.*)")
re_date = re.compile("Date:   (.*)")
re_version = re.compile("rustc [0-9\.a-zA-Z\-]* \(([0-9a-zA-Z]*) ([0-9\-]*)\) ")
re_rustc = re.compile("rustc: .*/(\w*)")
re_time = re.compile("( *)time: ([0-9\.]*)\s*(.*)")


def process(label, arg, n):
    for i in range(0, n):
        in_name = os.path.join('raw', '%s_%s_%s.log'%(label, arg, i))
        out_name = os.path.join('processed', '%s_%s_%s.json'%(label, arg, i))
        if VERBOSE:
            print "input:", in_name
            print "output:", out_name

        with open(in_name) as in_file:
            with open(out_name, 'w') as out_file:
                process_file(in_file, out_file)



def process_file(in_file, out_file):
    data = {}
    data['header'] = mk_header(in_file)
    data['times'] = mk_times(in_file)

    json.dump(data, out_file, indent=4)



def mk_header(in_file):
    commit_line = in_file.readline()
    if commit_line.startswith('rustc'):
        return mk_header_from_version(commit_line)

    # skip merge and author lines
    author_line = in_file.readline()
    if author_line.startswith('Merge'):
        in_file.readline()
    date_line = in_file.readline()

    header = {}
    header['commit'] = re_commit.match(commit_line).group(1)
    header['date'] = re_date.match(date_line).group(1)

    return header


def mk_header_from_version(version_line):
    match = re_version.match(version_line)
    header = {}
    header['commit'] = match.group(1)
    header['date'] = match.group(2)

    return header


def mk_times(in_file):
    all_times = []
    # The last mentioned crate being compiled.
    last_file = None
    cur_times = None
    for line in in_file:
        time_match = re_time.match(line)
        if time_match:
            assert(last_file)
            if not cur_times:
                cur_times = {}
                cur_times['crate'] = last_file
                cur_times['times'] = []
            indent = time_match.group(1)
            time = time_match.group(2)
            label = time_match.group(3)
            # TODO do something with 'sub-times'
            if not indent:
                cur_times['times'].append((label, float(time)))
        elif cur_times:
            all_times.append(process_times(cur_times))
            cur_times = None
            last_file = None

        rustc_match = re_rustc.match(line)
        if rustc_match:
            last_file = rustc_match.group(1)

    return all_times


def process_times(times):
    total = 0
    llvm = 0
    for (l, t) in times['times']:
        total += t
        if l in ['translation', 'LLVM passes', 'linking']:
            llvm += t

    times['total'] = total
    new_times = {}

    for (l, t) in times['times']:
        time = {
            'time': t,
            'percent': (t/total)*100,
            'ratio_llvm': (t/llvm)
        }
        new_times[l] = time

    times['times'] = new_times
    return times



if len(sys.argv) <= 3:
    print "Requires label, filename of log, and number of logs as arguments"
    exit(1)

process(sys.argv[1], sys.argv[2], int(sys.argv[3]))
