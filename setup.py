# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages
from distutils.core import setup

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '0.1.1'

setup(
    name='django-rulez',
    version=version,
    description="Flexible per-object authorization backend for Django",
    long_description=read('README.rst'),
    classifiers=[
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        "Framework :: Django",
        "Environment :: Web Environment",
    ],
    keywords=['authorization', 'backends', 'django', 'rules', 'permissions', 'rulez'],
    author='Christopher Glass',
    author_email='tribaal@gmail.com',
    url='http://github.com/cglass/django-rulez',
    license='BSD',
    packages=find_packages(),
    zip_safe=False,
)
