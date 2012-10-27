#!/usr/bin/env python

import sys
from collections import Counter

class DB:
    # Commands are implicity mapped to methods of the same name, but lowercased.
    commands = ['SET', 'GET', 'UNSET', 'NUMEQUALTO', 'BEGIN', 'ROLLBACK', 'COMMIT', 'END']
    store = {}

    def run(self, query):
        """Runs the provided query and returns the result."""
        tokens = query.split(' ')
        command, args = tokens[0], tokens[1:]

        if command in self.commands:
            try:
                return DB.__dict__[command.lower()](self, *args)
            except TypeError:
                return '[ERROR] Probably incorrect arguments for command: %s' % command
        else:
            return '[ERROR] Unrecognized command: %s' % command

    def set(self, key, value):
        """SET [name] [value]: Set a variable [name] to the value [value].

        Neither variable names or values will ever contain spaces.
        """
        self.store[key] = value

    def get(self, key):
        """GET [name]: Print out the value stored under the variable [name].

        Print NULL if that variable name hasn't been set.
        """
        return self.store[key] if self.store.has_key(key) else 'NULL'

    def unset(self, key):
        """UNSET [name]: Unset the variable [name]."""
        if self.store.has_key(key):
            del self.store[key]

    def numequalto(self, value):
        """NUMEQUALTO [value]: Return the number of variables equal to [value].

        If no values are equal, this should output 0.
        """
        return Counter(v for k, v in self.store.iteritems())[value]

    def begin(self):
        """BEGIN: Open a transactional block."""
        pass

    def rollback(self):
        """ROLLBACK: Rollback all of the commands from the most recent transaction block.

        If no transactional block is open, print out INVALID ROLLBACK.
        """
        pass

    def commit(self):
        """COMMIT: Permanently store all of the operations from any presently
        open transactional blocks.
        """
        pass

    def end(self):
        """END: Exit the program."""
        sys.exit()

if __name__ == '__main__':
    db = DB()

    while True:
        query = raw_input().strip()
        if query != None:
            result = db.run(query)
            if result != None:
                print result
