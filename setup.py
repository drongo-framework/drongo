#!/usr/bin/env python

from setuptools import find_packages, setup


setup(
    name='drongo',
    version='1.0.0a1',
    description='A nano web-framework for python.',
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
    install_requires=[
        'six'
    ],
    zip_safe=False,
)
