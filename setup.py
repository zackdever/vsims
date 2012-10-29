#!/usr/bin/env python

from distutils.core import Command, setup

class TestCommand(Command):
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        from test import test_thumbtack_examples
        test_thumbtack_examples.test()

setup(
    name='vsims',
    version='0.1',
    description='A very simple in-memory key-value store, built for http://www.thumbtack.com/challenges',
    author='Zack Dever',
    author_email='zack@zackdever.com',
    url='https://github.com/zever/vsims',
    packages=['vsims',],
    license=open('LICENSE').read(),
    long_description=open('README.md').read(),
    cmdclass={'test': TestCommand},
)

