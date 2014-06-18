from setuptools import setup, find_packages
import sys, os

version = '0.0.1'

setup(name='Adengine',
      version=version,
      description="CRUD ads",
      long_description="""\
Create/Read/Update/Delete ads""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='ad nothing too exited',
      author='Space Cowboys unlished',
      author_email='',
      url='http://github.com',
      license='Artistic 2.0',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=True,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
