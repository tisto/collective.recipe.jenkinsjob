# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.jenkinsjob
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    with open(os.path.join(os.path.dirname(__file__), *rnames), 'rb') as text:
        return text.read().decode('utf-8')

version = '1.0-alpha1'

description = "Buildout recipe to manage jobs on a remote Jenkins CI server."

long_description = (
    read('README.rst')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Download\n'
    '********\n')

entry_point = 'collective.recipe.jenkinsjob:Recipe'
entry_points = {
    "zc.buildout": ["default = %s" % entry_point],
}

tests_require = [
    'zope.testing',
    'zc.buildout [test]',
    'mocker'
]

setup(name='collective.recipe.jenkinsjob',
      version=version,
      description=description,
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
          'Framework :: Buildout',
          'Intended Audience :: Developers',
          'Topic :: Software Development :: Build Tools',
      ],
      keywords='',
      author='Domen Kozar and Timo Stollenwerk',
      author_email='domen@dev.si',
      url='https://github.com/tisto/collective.recipe.jenkinsjob',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'zc.buildout',
          'python-jenkins <= 0.3.99 ,>= 0.3.4',
          'zc.recipe.egg',
          'six >= 1.8.0',       # Required by python-jenkins but not declared.
          'collective.recipe.template',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='collective.recipe.jenkinsjob.tests.test_docs.test_suite',
      entry_points=entry_points,
)
