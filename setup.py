# -*- coding: utf-8 -*-
# Pythonic SQL
# Copyright (C) 2019 alvations

from distutils.core import setup

setup(
    name='dopplershift',
    version='0.0.2',
    packages=['dopplershift'],
    description='Pythonic SQL for mere mortals.',
    long_description='',
    install_requires=[
        "numpy",
        'psycopg2',
    ],
    url = 'https://github.com/alvations/dopplershift',
    license="MIT"
)
