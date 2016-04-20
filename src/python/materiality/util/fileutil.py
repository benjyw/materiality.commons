# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from contextlib import contextmanager
import os


@contextmanager
def umask(mask):
  orig_umask = os.umask(mask)
  yield
  os.umask(orig_umask)


@contextmanager
def backup(path):
  if os.path.exists(path):
    bak = path + '.bak'
    os.rename(path, bak)
    yield bak  # Caller decides when to delete bak.
  else:
    yield None


@contextmanager
def cwd(path):
  orig_cwd = os.getcwd()
  os.chdir(path)
  yield
  os.chdir(orig_cwd)
