from collections import Counter

class NestedStore:
    blocks = [{}]
    base = blocks[0]

    def set(self, key, value):
        self.blocks[-1][key] = value

    def get(self, key):
        for block in reversed(self.blocks):
            if block.has_key(key):
                return block[key]

    def has_key(self, key):
        for block in reversed(self.blocks):
            if block.has_key(key):
                return True

        return False

    def delete(self, key):
        #TODO deletes neeed to be localized to this block
        for block in reversed(self.blocks):
            if block.has_key(key):
                del block[key]

    def nest(self):
        self.blocks.append({})

    def pop_nest(self):
        self.blocks.pop()

    def flatten(self):
        for block in self.blocks:
            for key, value in block.iteritems():
                self.base[key] = value

        self.blocks = self.blocks[:1]

    def is_flat(self):
        return len(self.blocks) == 1

    def numequalto(self, value):
        #TODO this isn't nested
        return Counter(v for k, v in self.blocks[-1].iteritems())[value]
