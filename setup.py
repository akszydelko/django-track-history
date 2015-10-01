from setuptools import setup, find_packages
from codecs import open
from os import path

root = path.abspath(path.dirname(__file__))
with open(path.join(root, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='django-track-history',
    version='0.0.1',
    description='Easy change tracking for Django',
    long_description=long_description,
    url='https://github.com/akszydelko/django-track-history',
    author='Arkadiusz Szydelko',
    author_email='akszydelko@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Environment :: Web Environment',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Framework :: Django',
        'Framework :: Django :: 1.8',
    ],
    keywords='django history',
    packages=find_packages(),
    install_requires=['django>=1.8', 'django-pgjsonb>=0.0.16'],
)