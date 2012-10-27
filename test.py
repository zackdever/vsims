#!/usr/bin/env python
# -*- coding: utf8 -*-

from db import DB

def test(name):
    """Tests results from running <name>input.txt against <name>output.txt.

    <name>input.txt - Each line in file is ran as a DB query.
    <name>output.txt - The output of running the queries should match this file.
    """
    print 'Running: %s' % name
    print '-' * 30

    queries = read_lines('./test/%sinput.txt' % name)
    expected = read_lines('./test/%soutput.txt' % name)
    results = run_queries(queries)
    win, fail = '✓', '✗'

    if len(expected) != len(results):
        print '%s - Output results differ in length' % fail
        print 'Expected\n', expected
        print 'Actual\n', results
    else:
        for i, result in enumerate(results):
            correct = expected[i]
            if str(result) == correct:
                print '%s - expected and actual: %s' % (win, correct)
            else:
                print '%s - expected: "%s", actual: "%s"' % (fail, correct, result)

    print 'Completed %s.' % name
    print ''

def run_queries(queries):
    """Runs each query and returns a list of results."""
    db = DB()
    results = []

    for query in queries:
        try:
            result = db.run(query)
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
    test('test3')


