#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'Click>=7.0',
    'numpy',
    'Pillow',
    # 'https://github.com/moodule/typical.git@v0.1.1#egg=typical',
    ]

setup_requirements = [
    'bump2version',
    'pyment',
    'pytest-runner',
    'twine',
    'watchdog',
    'wheel',
    'Sphinx', ]

test_requirements = [
    'coverage',
    'flake8',
    'hypothesis',
    'pytest>=3',
    'tox', ]

setup(
    author="David Mougeolle",
    author_email='david.mougeolle@gmail.com',
    python_requires='>=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*, !=3.4.*',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="Upcycle your old books into beautiful art! :arrow_up_small:",
    entry_points={
        'console_scripts': [
            'overworked=overworked.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='upcycling diy blueprint book art',
    name='overworked',
    packages=find_packages(include=['overworked', 'overworked.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/moodule/overworked',
    version='0.6.2',
    zip_safe=False,
)
