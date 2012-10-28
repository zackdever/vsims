#!/usr/bin/env python

import sys
from nestedstore import NestedStore

class DB:
    """A simple in-memory key-value store with nested transactional blocks."""

    # Commands are implicity mapped to methods of the same name, but lowercased.
    commands = ['SET', 'GET', 'UNSET', 'NUMEQUALTO', 'BEGIN', 'ROLLBACK', 'COMMIT', 'END']

    def __init__(self):
        self.store = NestedStore()

    def run(self, query):
        """Runs the provided query and returns the result."""
        tokens = query.split(' ')
        command, args = tokens[0], tokens[1:]

        if command in DB.commands:
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
        self.store.set(key, value)

    def get(self, key):
        """GET [name]: Print out the value stored under the variable [name].

        Print NULL if that variable name hasn't been set.
        """
        return self.store.get(key) if self.store.has_key(key) else 'NULL'

    def unset(self, key):
        """UNSET [name]: Unset the variable [name]."""
        self.store.delete(key)

    def numequalto(self, value):
        """NUMEQUALTO [value]: Return the number of variables equal to [value].

        If no values are equal, this should output 0.
        """
        return self.store.numequalto(value)

    def begin(self):
        """BEGIN: Open a transactional block."""
        self.store.nest()

    def rollback(self):
        """ROLLBACK: Rollback all of the commands from the most recent transaction block.

        If no transactional block is open, print out INVALID ROLLBACK.
        """
        if self.store.is_flat():
            return 'INVALID ROLLBACK'
        else:
            self.store.pop_nest()

    def commit(self):
        """COMMIT: Closes all open transactional blocks."""
        self.store.flatten()

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
