# -*- coding: utf-8 -*-
"""
This module contains the tool of hai.pnp
"""
import os
from setuptools import setup, find_packages

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '1.0beta'

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    read('hai', 'pnp', 'README.txt')
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n' +
    'Download\n'
    '********\n'
    )

tests_require=['zope.testing']

setup(name='hai.pnp',
      version=version,
      description="Content types and workflows for HAI's policies and procedures",
      long_description=long_description,
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        'Framework :: Plone',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        ],
      keywords='',
      author='Jesse Snyder',
      author_email='consulting@npowerseattle.org',
      url='http://trac.npowerseattle.org/hai_project',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['hai', ],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'Products.OrderableReferenceField'
                        ],
      tests_require=tests_require,
      extras_require=dict(tests=tests_require),
      test_suite = 'hai.pnp.tests.test_docs.test_suite',
      entry_points="""
      """,
      )
