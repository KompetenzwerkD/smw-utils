#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from os.path import dirname, abspath, join

base_path = dirname(abspath(__file__))

with open(join(base_path, "README.md")) as readme_file:
    readme = readme_file.read()

with open(join(base_path, "requirements.txt")) as req_file:
    requirements = req_file.readlines()

setup(
    name="smw_utils",
    description='Some python utils for importing and exporting data in (semantic) mediawiki',
    long_description=readme,
    license="MIT",
    author='KompetenzwerkD',
    author_email='kompetenzwerkd@saw-leipzig.de',
    url='https://github.com/kompetenzwerkd/smw_utils',
    packages=find_packages(exclude=['dev', 'docs']),
    package_dir={
            'smw_utils': 'smw_utils'
        },
    version="0.0.1",
    py_modules=["smw_utils"],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',        
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: PyPy',

    ],
    keywords=[
        'meantic mediawiki', 'mediawiki'
    ],
)