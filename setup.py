#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
from setuptools import setup

setup(name="kmx_cli",
      version='0.1.0',
      packages=[
          'kmx_cli'
      ],
      description='Command line interface for KMX',
      author='Yang Rui',
      author_email='yangrui@k2data.com.cn',
      url='http://www.k2data.com.cn',
      install_requires=[
          'colorama==0.3.1',
          'sqlparse==0.2.0',
          'requests==2.7.0',
          'arrow==0.8.0',
          # 'tabulate==0.7.5',
          'wcwidth==0.1.7'
      ],
      entry_points={
          'console_scripts': [
            'kmx=kmx_cli.cli:run'
          ]
      }
      )
