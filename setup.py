# -*- coding: utf8 -*-
"""
A setuptools based setup module.

See:
https://packaging.python.org/en/latest/distributing.html
https://github.com/pypa/sampleproject
"""


from setuptools import setup, find_packages
import codecs
import os


long_description="""\
Pylatest project provides a set of tools which allows you to:

* Write a description of a test case using reStructuredText syntax.
* Include this description into a python source code directly, where it can
  be split into individual sections or actions to be performed, so that the
  description and test automation code are stored next to each other.

The reason behind this is to make synchronization between automatic test cases
and test case description documents simple while keeping the maintenance cost
low in the long term.
"""

setup(
    name='pylatest',
    # See https://packaging.python.org/en/latest/distributing/#choosing-a-versioning-scheme
    # TODO: connect with git tags?
    version='0.0.5.dev1',
    description='Testcase description generation tools.',
    long_description=long_description,
    url='http://github.com/mbukatov/pylatest/',
    author='Martin Bukatovič',
    author_email='mbukatov@redhat.com',
    license='GPLv3',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Software Development :: Quality Assurance',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        ],
    packages=find_packages(exclude=['doc', 'tests']),
    install_requires=['docutils'],
    # TODO: make this work with git (and remove MANIFEST.in?)
    # setup_requires=['setuptools_scm'],
    # use_scm_version=True,
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'pylatest-template=pylatest.template:main',
            'py2pylatest=pylatest.pysource:main',
            'pylatest2html=pylatest.main:pylatest2html',
            'pylatest2htmlplain=pylatest.main:pylatest2htmlplain',
            'pylatest2man=pylatest.main:pylatest2man',
        ],
    },
    test_suite = 'tests',
    )
