#!/usr/bin/env python

from setuptools import find_packages, setup
from drongo.version import __version__


setup(
    name='drongo',
    version=__version__,
    description='A pico web-framework for python.',
    author='Sattvik Chakravarthy',
    author_email='sattvik@gmail.com',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
