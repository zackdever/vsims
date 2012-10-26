#!/usr/bin/env python

import sys
from collections import Counter

class DB:
    store = {}

    def run(self, query):
        tokens = query.split(' ')
        command = tokens[0]
        args = tokens[1:]

        if command == 'SET':
            self.set(*args)
        elif command == 'GET':
            self.get(*args)
        elif command == 'UNSET':
            self.unset(*args)
        elif command == 'NUMEQUALTO':
            self.numequalto(*args)
        elif command == 'END':
            self.end(*args)
        else:
            print '[ERROR] Unrecognized command:', command

    def set(self, key, value):
        """SET [name] [value]: Set a variable [name] to the value [value].

        Neither variable names or values will ever contain spaces.
        """
        self.store[key] = value

    def get(self, key):
        """GET [name]: Print out the value stored under the variable [name].

        Print NULL if that variable name hasn't been set.
        """
        print self.store[key] if self.store.has_key(key) else 'NULLL'

    def unset(self, key):
        """UNSET [name]: Unset the variable [name]."""
        del self.store[key]

    def numequalto(self, value):
        """NUMEQUALTO [value]: Return the number of variables equal to [value].

        If no values are equal, this should output 0.
        """
        print Counter(v for k, v in self.store.iteritems())[value]

    def end(self):
        """END: Exit the program."""
        sys.exit

if __name__ == '__main__':
    db = DB()

    for line in sys.stdin:
        line = line.strip()
        if line:
            db.run(line)
