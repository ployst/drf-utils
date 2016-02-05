#!/usr/bin/env python
# coding: utf-8

from setuptools import setup
import os

__version__ = '{{VERSION}}'


DIR = os.path.dirname(__file__)


if __name__ == '__main__':
    setup(
        name='drf-utils',
        description=(
            'Reusable utilities for DRF used at Ployst'
        ),
        long_description=open(os.path.join(DIR, 'README.md')).read(),
        version=__version__,
        author='The ployst team',
        author_email='dev@ployst.com',
        url='https://github.com/ployst/drf-utils',
        packages=['drfutils', 'drfutils.migrations'],
        package_data={
            '': ['*.md'],
        },
        classifiers=[
            'Environment :: Console',
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 2',
            'Programming Language :: Python :: 2.7',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.2',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.4',
            'Topic :: Software Development :: Libraries',
        ],
    )
