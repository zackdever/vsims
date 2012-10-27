#!/usr/bin/env python

import sys
from collections import Counter

class DB:
    store = {}

    def run(self, query):
        tokens = query.split(' ')
        command = tokens[0]
        args = tokens[1:]

        try:
            if command == 'SET':
                return self.set(*args)
            elif command == 'GET':
                return self.get(*args)
            elif command == 'UNSET':
                return self.unset(*args)
            elif command == 'NUMEQUALTO':
                return self.numequalto(*args)
            elif command == 'END':
                return self.end(*args)
            else:
                return '[ERROR] Unrecognized command: %s' % command
        except TypeError:
            return '[ERROR] Probably incorrect arguments for command: %s' % command

    def set(self, key, value):
        """SET [name] [value]: Set a variable [name] to the value [value].

        Neither variable names or values will ever contain spaces.
        """
        self.store[key] = value

    def get(self, key):
        """GET [name]: Print out the value stored under the variable [name].

        Print NULL if that variable name hasn't been set.
        """
        return self.store[key] if self.store.has_key(key) else 'NULLL'

    def unset(self, key):
        """UNSET [name]: Unset the variable [name]."""
        if self.store.has_key(key):
            del self.store[key]

    def numequalto(self, value):
        """NUMEQUALTO [value]: Return the number of variables equal to [value].

        If no values are equal, this should output 0.
        """
        return Counter(v for k, v in self.store.iteritems())[value]

    def end(self):
        """END: Exit the program."""
        sys.exit()

if __name__ == '__main__':
    db = DB()

    while True:
        line = raw_input().strip()
        if line != None:
            result = db.run(line)
            if result != None:
                print result
