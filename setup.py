#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'requests==2.22.0',
                'pandas==0.24.2', 'rarfile==3.0',
                'beautifulsoup4==4.7.1', 'unrar==0.3']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Mayra Azevedo",
    author_email='mayradazevedo@ufrn.edu.br',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: Portuguese',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="API de dados abertos da PRF",
    entry_points={
        'console_scripts': [
            'prf_api=prf_api.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords=['prf', 'wrapper'],
    name='prf_api',
    packages=find_packages(include=['prf_api']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/nymarya/prf_api',
    version='0.2.0',
    zip_safe=False,
)
