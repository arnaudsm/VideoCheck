#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

requirements = ['Click>=7.0', 'pandas', 'tqdm']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

with open("README.MD", "r") as fh:
    long_description = fh.read()

setup(
    author="Arnaud de Saint Meloir",
    author_email='arnaud.desaintmeloir@gmail.com',
    python_requires='>=3.5',
    description="Automated tool to check consistency of your video library.",
    entry_points={
        'console_scripts': [
            'videocheck=videocheck.cli:main',
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description_content_type="text/markdown",
    long_description=long_description,
    include_package_data=True,
    keywords='videocheck',
    name='videocheck',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/arnaudsm/videocheck',
    version='0.1.1',
    zip_safe=True,
)
