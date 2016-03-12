# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os

import django
from django.conf import settings


# At module scope, so we're sure it only happens once.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')
django.setup()


def get_django_settings():
  """Returns the django settings to standalone scripts running outside the django framework."""
  return settings
