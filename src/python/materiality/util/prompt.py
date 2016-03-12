# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from contextlib import contextmanager
import os
import sys

from django.utils.crypto import get_random_string


# This code may be used in the script that creates the venv, and so can't rely on any deps existing.
# Still, we try to import from colors, in case we have it, as a nice-to-have.
try:
  from colors import green
except ImportError:
  green = lambda x: x


def confirm(prompt):
  prompt += ' [y/N] '
  answer = raw_input(green(prompt)).lower()
  return answer in ['y', 'yes']


def confirm_or_exit(prompt):
  if not confirm(prompt):
    sys.exit(1)


def get_secret_string(name, generator_length):
  have_value = confirm("Do you have an existing {0}? (If not, I'll generate one)".format(name))
  if have_value:
    secret_string = raw_input(green('Paste {0}: '.format(name)))
  else:
    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    secret_string = get_random_string(generator_length, chars)
  return secret_string


def get_secret_key():
  return get_secret_string('Django SECRET_KEY', 50)


def get_database_password():
  return get_secret_string('database password', 32)
