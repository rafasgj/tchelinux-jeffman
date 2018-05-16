#!/usr/bin/env python3

"""Load a CSV file with lectures and provide a JSON file."""

import json
import csv
import sys
import re


def load_data(eventfile):
    """Load data from file."""
    lectures = {}
    fields = ["room", "author", "title", "abstract", "keywords",
              "level", "resume", "topic", "email", "fone"]
    with open('data/%s.csv' % eventfile) as csvfile:
        for row in csv.reader(csvfile):
            if re.search(r'timestamp', "".join(row), re.I):
                continue
            if row[0] == '':
                continue
            if row[0][0] != '1':
                row[0] = '0'+row[0]
            p = {k: v for k, v in zip(fields, row[1:10])}
            lectures.setdefault(row[0], []).append(p)
    return lectures


def load_event(eventfile):
    """Load an event."""
    with open('data/%s.json' % eventfile) as jf:
        return json.load(jf)


if len(sys.argv) < 2:
    print("usage: palestras_json.py <codinome>\n")
    msg = "Nao esqueca de adicionar os aquivos JSON e CSV ao diretario 'data'"
    print(msg)
    sys.exit()

lectures = load_data(sys.argv[1])
event = load_event(sys.argv[1])
event['schedule'] = lectures

print(json.dumps(event, sort_keys=True, indent=4))
