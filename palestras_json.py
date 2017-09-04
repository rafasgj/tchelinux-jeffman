#!/usr/bin/env python3

import json
import csv
import sys
import re
from functools import reduce

def load_data(eventfile):
    lectures = {}
    fields = ["room", "author", "title", "abstract", "keywords", "level", "resume"]
    with open('data/%s.csv'%eventfile) as csvfile:
        for row in csv.reader(csvfile):
            if re.search(r'timestamp',"".join(row),re.I): continue
            passed_header = True
            if row[0] == '': continue
            p = { k:v for k,v in zip(fields,row[1:8]) }
            lectures.setdefault(row[0],[]).append(p)
    return lectures

def load_event(eventfile):
    with open('data/%s.json'%eventfile) as jf:
        return json.load(jf)

if len(sys.argv) < 2:
    print ("usage: palestras_json.py <codinome>")
    print ("\nNao esqueca de adicionar os aquivos JSON e CSV ao diretario 'data'")
    sys.exit()

lectures = load_data(sys.argv[1])
event = load_event(sys.argv[1])
event['schedule'] = lectures

print(json.dumps(event, sort_keys=True, indent=4))
