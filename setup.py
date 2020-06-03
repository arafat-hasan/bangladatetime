#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# def readme():
# with open("README", 'r') as f:
#     long_description = f.read()

# long_description = "bangla DateTime"
# return long_description
readme = open('README.rst').read()

setup(
    # Metadata
    name='bangladatetime',
    version='0.1c1',
    author='Arafat Hasan',
    author_email='opendoor.arafat@gmail.com',
    url="https://github.com/arafat-hasan/bangladatetime/",
    description='Python package for Bengali (i.e Bangabdo) date and time',
    long_description=readme,
    license="MIT",
    keywords="bangla bangla-date bongabdo bengali bengali-date "
        "bengalidatetime bangladatetime",
    packages=find_packages(exclude=('tests',)),
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Bengali",
    ],
)