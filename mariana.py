#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""This script consumes the API from Mariaweb to be used with mbot-shell."""

import sys
import re
import requests
import mylib

TIMEOUT = 1.5

def format_message(record):
    """Returns a formatted string ready for output."""
    return "%s - #%s, %s [%s]" % \
        (record['text'], record['user'], record['datetime'], record['magazine'][:1].lower())

def random_message():
    """Returns a random message."""
    request = requests.get('https://maria.deadbsd.org/api/random', timeout=TIMEOUT)
    json = request.json()

    message = json['message']
    return format_message(message)

def find_message(text=None, user=None, position=1):
    """Finds message based on text or userId."""
    out = ""
    params = {'position': int(position)}
    if text:
        params['text'] = text
    if user:
        params['user'] = user

    request = requests.get('https://maria.deadbsd.org/api/find', params, timeout=TIMEOUT)
    json = request.json()

    if 'error' in json:
        out = json['error']
    else:
        total = json['total']
        if total > 1 and position < total:
            mylib.print_console("%d found '.fm %s %d' for the next one" % \
                (total, text or user, json['next']))

        record = json['message']
        out = format_message(record)
    return out

def latest_message(position=1):
    """Returns the latest message."""
    out = ""
    params = {'position': int(position)}

    request = requests.get('https://maria.deadbsd.org/api/latest', params, timeout=TIMEOUT)
    json = request.json()

    if 'error' in json:
        out = json['error']
    else:
        total = json['total']
        if total > 1 and position < total:
            mylib.print_console("%d found '.fl %d' for the next one" % (total, json['next']))

        record = json['message']
        out = format_message(record)
    return out

if __name__ == "__main__":
    if len(sys.argv) == 1:
        mylib.print_console(random_message())
    if len(sys.argv) > 1:
        COMMAND = sys.argv[1]
        ARGS = ' '.join(sys.argv[2:])
        START = 1

        if COMMAND == "find":
            KEY = None
            NUMBER = None

            MATCH = re.search(r"^(?P<key>.*?)(?P<start> \d+)?$", ARGS)
            if MATCH.group('key'):
                KEY = MATCH.group('key')
            if MATCH.group('start'):
                START = int(MATCH.group('start').strip())

            try:
                userId = int(KEY)
                mylib.print_console(find_message(None, userId, START))
            except ValueError:
                mylib.print_console(find_message(KEY, None, START))
        elif COMMAND == "lista":
            if ARGS.isdigit():
                START = int(ARGS.strip())
            mylib.print_console(latest_message(START))
        elif COMMAND == "magia":
            mylib.print_console(random_message())
        else:
            mylib.print_console(random_message())
