#!/usr/bin/env python
from setuptools import setup, find_packages
from track_history import __version__

long_description = """
    A simple model change tracking for Django.
    
    More on: https://github.com/akszydelko/django-track-history
    
    Copyright (c) 2017, Arkadiusz Szydełko All rights reserved.

    Licensed under BSD 3-Clause License
    """

setup(
    name='django-track-history',
    version=__version__,
    description='Easy model change tracking for Django',
    long_description=long_description,
    url='https://github.com/akszydelko/django-track-history',
    author='Arkadiusz Szydelko',
    author_email='akszydelko@gmail.com',
    license='BSD',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Framework :: Django',
        'Framework :: Django :: 1.10',
    ],
    keywords='django track history',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'django>=1.10',
        'django-pgjsonb>=0.0.30'
    ],
)
