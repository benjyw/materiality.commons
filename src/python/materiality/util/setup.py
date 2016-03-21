# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import argparse


class Setup(object):
  local_settings_file = 'main/settings_local.py'

  @classmethod
  def register_cmd_line_args(cls, parser):
    parser.add_argument('--app-name', help='The name of the app.')
    parser.add_argument('--twitter-api', action='store_true', help='Whether this app uses the Twitter API.')

  @classmethod
  def create(cls, **kwargs):
    parser = argparse.ArgumentParser(description='Set up a materiality-based app.')
    cls.register_cmd_line_args(parser)
    ns = argparse.Namespace(**kwargs)  # Initialize with the kwargs.
    args = parser.parse_args(namespace=ns)  # Add in any flag values, overriding as needed.
    return cls(args)

  def __init__(self, args):
    if not args.app_name:
      raise Exception('app name must be specified.')
    self._args = args

  @property
  def app_name(self):
    return self._args.app_name

  @property
  def twitter_api(self):
    return self._args.twitter_api
