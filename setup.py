#!/usr/bin/env python
# -*- coding: utf-8 -*-
import django_logutils

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

version = django_logutils.__version__ 

readme = open('README.rst').read()
history = open('HISTORY.rst').read().replace('.. :changelog:', '')

setup(
    name='django-logutils',
    version=version,
    description="""Various logging-related utilities for Django projects.""",
    long_description=readme + '\n\n' + history,
    author='Sander Smits',
    author_email='jhmsmits@gmail.com',
    url='https://github.com/jsmits/django-logutils',
    packages=[
        'django_logutils',
    ],
    include_package_data=True,
    install_requires=[
        'django',
        'django-appconf'
    ],
    license="BSD",
    zip_safe=False,
    keywords='django-logutils',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
    ],
)
