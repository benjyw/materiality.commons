# coding=utf-8
# Copyright 2016 Materiality Labs.

# Note that setup expects string literals throughout and can fail in odd ways if provided with unicode.

from setuptools import setup, find_packages


setup(
  name = 'materiality.commons',
  packages = find_packages('src/python'),
  package_dir = {'': 'src/python'},
  install_requires=[
    'ansicolors>=1.0.2,<2.0',
    'Django>=1.7,<2.0',
    'newrelic>=2.60,<3.0',
    'psycopg2>=2.6,<3.0',
    'requests>=2.8,<3.0',
  ],
  test_suite='materiality.commons',
  version = '0.1.8',
  description = "Common code for Materiality Labs's Django/Postgres apps.",
  author = 'Benjy Weinberger',
  author_email = 'benjyw@gmail.com',
  license = 'MIT',
  url = 'https://github.com/materiality/commons',
  keywords = ['materiality', 'commons', 'django', 'postgres', 'pgsql', 'heroku'],
  classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Framework :: Django :: 1.7',
    'Framework :: Django :: 1.8',
    'Framework :: Django :: 1.9',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Application Frameworks',
  ],
)
