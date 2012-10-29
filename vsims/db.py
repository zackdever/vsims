#!/usr/bin/env python

import sys

from vsims.nestedstore import NestedStore

class DB:
    """A simple in-memory key-value store with nested transactional blocks."""

    # Commands are implicity mapped to methods of the same name, but lowercased.
    _commands_ = ['SET', 'GET', 'UNSET', 'NUMEQUALTO', 'BEGIN', 'ROLLBACK', 'COMMIT', 'END']

    def __init__(self):
        self._store_ = NestedStore()

    def run(self, query):
        """Runs the provided query and returns the result."""
        tokens = query.split(' ')
        command, args = tokens[0], (self._parse_token_(token) for token in tokens[1:])

        if command in DB._commands_:
            try:
                return DB.__dict__[command.lower()](self, *args)
            except TypeError:
                return '[ERROR] Probably incorrect arguments for command: {}'.format(command)
        else:
            return '[ERROR] Unrecognized command: {}'.format(command)

    def set(self, key, value):
        """SET [name] [value]: Set a variable [name] to the value [value].

        Neither variable names or values will ever contain spaces.
        """
        self._store_.set(key, value)

    def get(self, key):
        """GET [name]: Print out the value stored under the variable [name].

        Print NULL if that variable name hasn't been set.
        """
        return self._store_.get(key) if self._store_.has_key(key) else 'NULL'

    def unset(self, key):
        """UNSET [name]: Unset the variable [name]."""
        self._store_.delete(key)

    def numequalto(self, value):
        """NUMEQUALTO [value]: Return the number of variables equal to [value].

        If no values are equal, this should output 0.
        """
        return self._store_.numequalto(value)

    def begin(self):
        """BEGIN: Open a transactional block."""
        self._store_.nest()

    def rollback(self):
        """ROLLBACK: Rollback all of the commands from the most recent transaction block.

        If no transactional block is open, print out INVALID ROLLBACK.
        """
        if self._store_.is_flat():
            return 'INVALID ROLLBACK'
        else:
            self._store_.pop_nest()

    def commit(self):
        """COMMIT: Closes all open transactional blocks."""
        self._store_.flatten()

    def end(self):
        """END: Exit the program."""
        sys.exit()

    def _parse_token_(self, token):
        """Converts the token into an int or float if applicable.

        token - the string to parse
        Returns the token as is, or as an int or float if possible.
        """
        try:
            return int(token)
        except ValueError:
            try:
                return float(token)
            except ValueError:
                return token


def shell():
    """A very simple shell."""
    db = DB()

    while True:
        query = sys.stdin.readline().strip()
        if query != None:
            result = db.run(query)
            if result != None:
                print result

if __name__ == '__main__':
    shell()
