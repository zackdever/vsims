#!/usr/bin/env python
# -*- coding: utf8 -*-

from db import DB

def test(name):
    """Tests results from running <name>input.txt against <name>output.txt.

    <name>input.txt - Each line in file is ran as a DB command.
    <name>output.txt - The output of running the input commands should match this file.
    """
    print 'Running: %s' % name
    print '-' * 30

    commands = read_lines('./test/%sinput.txt' % name)
    expected = read_lines('./test/%soutput.txt' % name)
    actual = run_commands(commands)
    win, fail = '✓', '✗'

    if len(expected) != len(actual):
        print '%s - Output lines differ in length' % fail
        print 'Expected\n', expected
        print 'Actual\n', actual
    else:
        for i, result in enumerate(actual):
            correct = expected[i]
            if str(result) == correct:
                print '%s - expected and actual: %s' % (win, correct)
            else:
                print '%s - expected: "%s", actual: "%s"' % (fail, correct, result)

    print 'Completed %s.' % name
    print ''

def run_commands(commands):
    """Runs each command and returns a list of results."""
    db = DB()
    results = []

    for command in commands:
        try:
            result = db.run(command)
            if result != None:
                results.append(result)
        except SystemExit:
            break

    return results

def read_lines(filename):
    """Read and sanitize lines in file."""
    lines = []

    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            if line:
                lines.append(line)

    return lines

if __name__ == '__main__':
    test('test1')
    test('test2')


