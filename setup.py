#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup


def readme():
    # with open("README", 'r') as f:
    #     long_description = f.read()

    long_description = "bangla DateTime"
    return long_description


setup(
    name='bangladatetime',
    version='0.1c1',
    description='bangla Date Time',
    license="MIT",
    long_description=readme(),
    keywords=
    'bangla bangla-date bongabdo bangla digit bangla bangla-date bangladatetime',
    author='Arafat Hasan',
    author_email='opendoor.arafat@gmail.com',
    url="https://github.com/arafat-hasan/bangladatetime/",
    packages=['bangladatetime'],
    install_requires=['bar', 'greek'],
    scripts=[
        'scripts/cool',
        'scripts/skype',
    ])
