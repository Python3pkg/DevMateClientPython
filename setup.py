#!/usr/bin/env python
import os

from setuptools import setup

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

requirements = [
    'requests >= 2.5.2, <= 2.11.1',
]

version = None
exec(open('devmateclient/version.py').read())

setup(
    name='devmateclient',
    version=version,
    description='Simple DevMate Public API client',
    url='https://github.com/DevMate/DevMateClientPython',
    author='Pavel Akimenko',
    author_email='kim@macpaw.com',
    license='MIT',
    packages=[
        'devmateclient',
        'devmateclient.api'
    ],
    install_requires=requirements,
    keywords=['devmate', 'api', 'client'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Other Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
)
