from collections import Counter

class Block:
    def __init__(self):
        self.ops = []

    def log(self, command, *args):
        self.ops.append((command, args))

    def rollback(self):
        for op in reversed(self.ops):
            op[0](*op[1])

class NestedStore:
    def __init__(self):
        self.store = {}
        self.blocks = []

    def set(self, key, value, doLog=True):
        if not self.is_flat() and doLog:
            block = self.blocks[-1]
            if self.has_key(key):
                block.log(self.set, key, self.get(key), False)
            else:
                block.log(self.delete, key, False)

        self.store[key] = value

    def get(self, key):
        return self.store[key]

    def has_key(self, key):
        return self.store.has_key(key)

    def delete(self, key, doLog=True):
        if self.has_key(key):
            if not self.is_flat() and doLog:
                self.blocks[-1].log(self.set, key, self.get(key), False)
            del self.store[key]

    def nest(self):
        self.blocks.append(Block())

    def pop_nest(self):
        self.blocks.pop().rollback()

    def flatten(self):
        self.blocks = []

    def is_flat(self):
        return len(self.blocks) == 0

    def numequalto(self, value):
        return Counter(v for k, v in self.store.iteritems())[value]
