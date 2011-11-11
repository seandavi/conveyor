from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(name='conveyor',
      version=version,
      description="Pipelines for NGS data",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='RNAseq NGS sequencing bioinformatics ruffus',
      author='Sean Davis',
      author_email='seandavi@gmail.com',
      url='http://github.com/seandavi/conveyor',
      license='GPL-2',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'ruffus',
          'pyyaml'
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
