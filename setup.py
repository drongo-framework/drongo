#!/usr/bin/env python

from setuptools import find_packages, setup


setup(
    name='drongo',
    version='1.2.0',
    description='A nano web-framework for python.',
    author='Sattvik Chakravarthy, Sagar Chakravarthy',
    author_email='sattvik@gmail.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
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
    url='https://github.com/drongo-framework/drongo',
    include_package_data=True,
    install_requires=[
        'passlib',
        'pymongo',
        'six',
    ],
    zip_safe=False,
)
