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
