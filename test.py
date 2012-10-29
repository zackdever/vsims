#!/usr/bin/env python

import unittest

from db import DB

class ThumbtackIntegrationTest(unittest.TestCase):
    def setUp(self):
        self.actual_output = []
        self.db = DB()

        # config
        self.longMessage = True
        self.test_data_dir = './test-data/'

    def test_basic_commands_1(self):
        """1st basic sample from http://www.thumbtack.com/challenges."""
        self.worker('basic-1')

    def test_basic_commands_2(self):
        """2nd basic sample from http://www.thumbtack.com/challenges."""
        self.worker('basic-2')

    def test_transactional_commands_1(self):
        """1st transactional sample from http://www.thumbtack.com/challenges."""
        self.worker('transactional-1')

    def test_transactional_commands_2(self):
        """2nd transactional sample from http://www.thumbtack.com/challenges."""
        self.worker('transactional-2')

    def test_transactional_commands_3(self):
        """3rd transactional sample from http://www.thumbtack.com/challenges."""
        self.worker('transactional-3')

    def test_transactional_commands_4(self):
        """4th transactional sample from http://www.thumbtack.com/challenges."""
        self.worker('transactional-4')

    def worker(self, title):
        """Tests output from running <title>-in.txt against <title>-out.txt.

        These txt files should be located in the directory: self.test_data_dir.
        """
        out_file = '{}{}-out.txt'.format(self.test_data_dir, title)
        expected_output = self.read_lines(out_file)

        queries = self.read_lines('{}{}-in.txt'.format(self.test_data_dir, title))
        self.run_queries(queries)
        self.assertEqual(len(self.actual_output), len(expected_output),
                'Query results differ in length from {}'.format(out_file))

        for i, actual in enumerate(self.actual_output):
            self.assertEqual(str(actual), expected_output[i],
                    'Query result line {} does not match {}'.format(i+1, out_file))

    def run_queries(self, queries):
        """Runs queries and stores the results."""
        for query in queries:
            try:
                result = self.db.run(query)
                if result != None:
                    self.actual_output.append(result)
            except SystemExit:
                break

    def read_lines(self, filename):
        """Read, sanitize, and return lines in file."""
        with open(filename, 'r') as f:
            return [line.strip() for line in f if line.strip() != None]

if __name__ == '__main__':
    unittest.main(verbosity=2)
