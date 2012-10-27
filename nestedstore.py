from collections import Counter

class Block:
    """A block of operations that can be called in reverse order.

    Use: To isolate a block of commands, before executing each command,
    log a command which will reverse it. Then if needed, simply rollback
    to undo that block."""

    def __init__(self):
        self.ops = []

    def log(self, command, *args):
        """Adds the command and arguments to the log.

        command - a function that will be called on rollback
        args - arguments to be supplied to the command on rollback
        """
        self.ops.append((command, args))

    def rollback(self):
        """Call all the logged commands in reverse order."""
        for op in reversed(self.ops):
            op[0](*op[1])

class NestedStore:
    """Simple key-value store that supports nested transactional blocks."""
    def __init__(self):
        self.store = {}
        self.blocks = []

    def set(self, key, value, doLog=True):
        """Add the key to the store if not already present, and set its value.

        key - key to add or update
        value - value set for key
        doLog - determines if a reverse operation should be logged
        """
        if not self.is_flat() and doLog:
            block = self.blocks[-1]
            if self.has_key(key):
                block.log(self.set, key, self.get(key), False)
            else:
                block.log(self.delete, key, False)

        self.store[key] = value

    def get(self, key):
        """Returns the value of the given key.

        throws: KeyError if key is not present in the store
        """
        return self.store[key]

    def has_key(self, key):
        """Determines if the store contains the key."""
        return self.store.has_key(key)

    def delete(self, key, doLog=True):
        """Deletes the key from the store if present.

        key - key to delete
        doLog - determines if a reverse operation should be logged
        """
        if self.has_key(key):
            if not self.is_flat() and doLog:
                self.blocks[-1].log(self.set, key, self.get(key), False)
            del self.store[key]

    def nest(self):
        """Start a new transactional block."""
        self.blocks.append(Block())

    def pop_nest(self):
        """End the currently open transactional block.

        throws: IndexError if there are no open transactional blocks.
        """
        self.blocks.pop().rollback()

    def flatten(self):
        """Permanently stores and closes all open transactional blocks."""
        self.blocks = []

    def is_flat(self):
        """Returns True if there are no open transactional blocks."""
        return len(self.blocks) == 0

    def numequalto(self, value):
        """Returns the number of keys set to the provided value."""
        return Counter(v for k, v in self.store.iteritems())[value]
