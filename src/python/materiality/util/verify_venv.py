# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import subprocess

# All other scripts run in a venv with the necessary deps installed. However this script creates that venv,
# and so can't rely on any deps existing. Still, we try to import from colors, in case we have it, as a nice-to-have.
try:
  from colors import green
except ImportError:
  green = lambda x: x

from materiality.util.execute import execute


_local_settings_file = 'main/settings_local.py'


def verify_virtualenv():
  print(green('Checking virtualenv version.'))
  try:
    execute('virtualenv --version')
  except (OSError, subprocess.CalledProcessError):
    print(green('Installing virtualenv.'))
    execute('sudo pip install "virtualenv>=1.11,<1.12"')
  print(green('virtualenv installed.'))


def verify_venv():
  verify_virtualenv()
  print(green('\nVerifying venv.'))
  try:
    print(green('Checking venv python version.'))
    execute('./venv/bin/python2.7 --version')
  except OSError, subprocess.CalledProcessError:
    print(green('Creating venv.'))
    execute('virtualenv venv')
  print(green('Venv created.\n'))


def verify_python_dependencies():
  print(green('\nVerifying python dependencies:'))
  execute('./venv/bin/pip install -r requirements.txt')
  print(green('Python dependencies installed.'))


def setup():
  verify_venv()
  verify_python_dependencies()
  print(green('Done!'))


if __name__ == '__main__':
  setup()
