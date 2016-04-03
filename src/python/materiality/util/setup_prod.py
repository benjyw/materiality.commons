# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os

from colors import green

from materiality.util.execute import execute, get_output
from materiality.util.prompt import get_secret_key
from materiality.util.setup_base import SetupBase


class SetupProd(SetupBase):
  @classmethod
  def register_cmd_line_args(cls, parser):
    super(SetupProd, cls).register_cmd_line_args(parser)
    parser.add_argument('--web-concurrency', type=int, default=4, help='How many concurrent gunicorn workers to run.')

  @staticmethod
  def get_current_heroku_config():
    lines = get_output('heroku config').strip().split('\n')[1:]
    split_lines = [line.split(':', 1) for line in lines]
    stripped_split_lines = [(k.strip(), v.strip()) for (k, v) in split_lines]
    return dict(stripped_split_lines)

  @classmethod
  def get_config_from_local_settings(cls, key):
    if os.path.exists(cls.local_settings_file):
      settings = {}
      execfile(cls.local_settings_file, settings)
      if key in settings:
        print(green('Reading {} from settings file.'.format(key)))
        return settings[key]
    print(green('{} not in local settings file.'.format(key)))
    return raw_input(green('Paste {}: '.format(key)))

  def update_heroku_config(self):
    current_config = self.get_current_heroku_config()

    def do_set(k, v):
      """Set only if the key doesn't exist."""
      if current_config.get(k) is None:
        if hasattr(v, '__call__'):
          v = v(k)
        execute('heroku config:set {}={}'.format(k, v))

    def do_update(k, v):
      """Set if the key doesn't exist, or update the value if it does."""
      if hasattr(v, '__call__'):
        v = v(k)
      if current_config.get(k) != v:
        execute('heroku config:set {}={}'.format(k, v))

    def do_update_from_local_settings(key):
      do_update(key, self.get_config_from_local_settings)

    do_set('SECRET_KEY', lambda(k): get_secret_key())
    do_update('{}_ENV'.format(self.app_name.upper()), '{}_prod'.format(self.app_name))
    do_update('WEB_CONCURRENCY', '{}'.format(self.args.web_concurrency))
    do_update('NEW_RELIC_APP_NAME', self.app_name)
    if self.twitter_api:
      do_update_from_local_settings('TWITTER_APP_ID')
      do_update_from_local_settings('TWITTER_APP_SECRET')
      do_update_from_local_settings('TWITTER_APP_SECRET')
    do_update_from_local_settings('NEWRELIC_API_KEY')
    for name in self.extra_local_settings():
      do_update_from_local_settings(name)
    for name, val in self.extra_configs():
      do_update(name, val)

  def update_buildpacks(self):
    execute('heroku buildpacks:clear')
    execute('heroku buildpacks:set heroku/python')
    for cmd in self.extra_buildpack_commands():
      execute(cmd)

  def enable_log_runtime_metrics(self):
    execute('heroku labs:enable log-runtime-metrics')

  def extra_buildpack_commands(self):
    """Override to add any extra buildpacks."""
    return []

  def extra_local_settings(self):
    """Override to provide names of any other local settings that should be copied to prod."""
    return []

  def extra_configs(self):
    """Override to provide (key, value) pairs of any other config vars that should be applied to prod.

    Value may be a callable, in which case the config var's value will be the result of calling value(key).
    """
    return []

  def setup(self):
    self.update_heroku_config()
    self.update_buildpacks()
    self.enable_log_runtime_metrics()


if __name__ == '__main__':
  SetupProd.create().setup()
