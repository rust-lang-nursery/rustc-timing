import os
import json

# read it
# try and find a corresponding rustc log file
# replace the date
# write it
def process(filename):
    idx = filename.find('--')
    suffix = filename[idx:]
    rustc_name = 'rustc' + suffix
    new_date = None

    try:
        with open(rustc_name) as rustc:
            rustc_json = json.load(rustc)
            new_date = rustc_json['header']['date']
    except Exception as e:
        print "couldn't find corresponding file for", filename
        print e

    log_json = None
    with open(filename, 'r') as log:
        log_json = json.load(log)
        log_json['header']['date'] = new_date
        
    with open(filename, 'w') as log:
        json.dump(log_json, log, indent=4)


# for each non-rustc log file
for f in os.listdir('.'):
    if f.endswith('.json') and not f.startswith('rustc--'):
        process(f)

