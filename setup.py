# -*- coding: utf-8 -*-
"""
This module contains the tool of collective.recipe.jenkinsjob
"""
import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0'

long_description = (
    read('README.rst')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('collective', 'recipe', 'jenkinsjob', 'README.txt')
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
    "console_scripts": [
#      "jenkins-job-build = collective.recipe.jenkinsjob:build_jenkins_job",
      'jenkins-job-pull = collective.recipe.jenkinsjob.pull:main',
    ]
}

tests_require = [
  'zope.testing',
  'zc.buildout',
  'mocker'
]

setup(name='collective.recipe.jenkinsjob',
      version=version,
      description="",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Buildout',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        ],
      keywords='',
      author='',
      author_email='',
      url='https://github.com/tisto/collective.recipe.jenkinsjob',
      license='gpl',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['collective', 'collective.recipe'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
        'setuptools',
        'zc.buildout',
        'python-jenkins',
        'zc.recipe.egg',
        'collective.recipe.template',
      ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite='collective.recipe.jenkinsjob.tests.test_docs.test_suite',
      entry_points=entry_points,
      )
