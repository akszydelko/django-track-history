#!/usr/bin/env python
from setuptools import setup, find_packages
from track_history import __version__

long_description = """
    A simple model change tracking for Django.

    More on: https://github.com/akszydelko/django-track-history

    Copyright (c) 2021, Arkadiusz Szydełko All rights reserved.

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
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Framework :: Django',
        'Framework :: Django :: 2.0',
        'Framework :: Django :: 2.1',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.0',
    ],
    keywords='django track history',
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'django>=2.0'
    ],
)
