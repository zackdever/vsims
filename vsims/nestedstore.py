from vsims.block import Block

class NestedStore:
    """Simple key-value store that supports nested transactional blocks."""
    def __init__(self):
        self.blocks = []
        self.store = {}
        self.value_counts = {}

    def set(self, key, value, doLog=True):
        """Add the key to the store if not already present, and set its value.

        key - key to add or update
        value - value set for key
        doLog - determines if a reverse operation should be logged
        """
        has_key = self.has_key(key)

        if not self.is_flat() and doLog:
            block = self.blocks[-1]
            if has_key:
                block.log(self.set, key, self.get(key), False)
            else:
                block.log(self.delete, key, False)

        if has_key:
            old_value = self.get(key)
            if old_value != value:
                self._update_value_count_(old_value, -1)
                self._update_value_count_(value, 1)
        else:
            self._update_value_count_(value, 1)

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

            self._update_value_count_(self.get(key), -1)
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
        if not self.value_counts.has_key(value):
            self.value_counts[value] = 0
            return 0

        return self.value_counts[value]

    def _update_value_count_(self, value, count):
        """Set or update the count for the provided value."""
        if self.value_counts.has_key(value):
            self.value_counts[value] += count
        else:
            self.value_counts[value] = count
