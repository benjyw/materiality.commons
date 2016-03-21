# coding=utf-8
# Copyright 2014 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os
import shutil
import sys


class Commander(object):
  class Error(Exception):
    pass

  @classmethod
  def is_forced(cls):
    if len(sys.argv) > 1:
      if sys.argv[1] == '--force':
        return True
      else:
        raise cls.Error('Usage: {0} [--force]'.format(sys.argv[0]))
    return False

  @classmethod
  def underline(cls, msg, underline_chr):
    print('')
    msg = msg.strip()
    print(msg)
    print(underline_chr * len(msg))

  @classmethod
  def header1(cls, msg):
    cls.underline(msg, '=')

  @classmethod
  def header2(cls, msg):
    cls.underline(msg, '-')

  @classmethod
  def are_you_sure(cls, prompt=''):
    if prompt:
      prompt += ' '
    prompt += 'Are you sure? [y/N]: '
    s = raw_input(prompt)
    return s.lower() in ['y', 'yes']

  @classmethod
  def are_you_sure_or_quit(cls, prompt=''):
    if not cls.are_you_sure(prompt):
      print('Quitting.')
      sys.exit(1)

  @classmethod
  def safe_rmtree(cls, directory):
     """Delete a directory if it's present. If it's not present, no-op."""
     if os.path.exists(directory):
       shutil.rmtree(directory, True)

  def __init__(self, force=False):
    self._tmp_data_dir = os.path.expanduser('~/innovata')
    self._force = force

  @property
  def tmp_data_dir(self):
    return self._tmp_data_dir

  @property
  def force(self):
    """Whether to restart all work from scratch, or pick up from last known good state."""
    return self._force

  def run(self):
    raise NotImplementedError('Subclasses must implement')
