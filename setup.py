#!/usr/bin/env python

import os
from setuptools import find_packages, setup

ENCODING = 'utf-8'
PACKAGE_NAME = 'alphavantage'

local_directory = os.path.abspath(os.path.dirname(__file__))
version_path = os.path.join(local_directory, PACKAGE_NAME, '_version.py')

version_ns = {}
with open(version_path, 'r', encoding=ENCODING) as f:
    exec(f.read(), {}, version_ns)


def get_requirements(requirement_file: str):
    requirements = list(
        open(requirement_file, 'r',
             encoding=ENCODING).read().strip().split('\r\n'))
    return requirements


def get_readme(readme_file: str):
    with open(readme_file, encoding='utf-8') as file:
        return file.read()


setup(name=PACKAGE_NAME,
      packages=find_packages(exclude=('tests',)),
      package_data={'': ['*.txt', '*.json']},
      include_package_data=True,
      version=version_ns['__version__'],
      license='MIT',
      description='Alphavantage API wrapper.',
      long_description=get_readme('README.md'),
      long_description_content_type='text/markdown',
      url='https://github.com/portfoliome/alphavantage',
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Financial and Insurance Industry',
          'Topic :: Office/Business :: Financial :: Investment',
          'Natural Language :: English',
          'Programming Language :: Python :: 3.6',
      ],
      author='Philip Martin',
      author_email='philip.martin@censible.co',
      install_requires=get_requirements('requirements.txt'),
      extras_require={
          'test': get_requirements('requirements-test.txt')
      },
      zip_safe=False)
