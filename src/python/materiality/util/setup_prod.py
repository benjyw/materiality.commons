# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os

from colors import green

from materiality.util.execute import execute, get_output
from materiality.util.prompt import get_secret_key
from materiality.util.setup import Setup


class SetupProd(Setup):
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

    def do_set(key, val):
      """Set only if the key doesn't exist."""
      if current_config.get(key) is None:
        if hasattr(val, '__call__'):
          val = val(key)
        execute('heroku config:set {}={}'.format(key, val))

    def do_update(key, val):
      """Set if the key doesn't exist, or update the value if it does."""
      if hasattr(val, '__call__'):
        val = val(key)
      if current_config.get(key) != val:
        execute('heroku config:set {}={}'.format(key, val))

    def do_update_from_local_settings(key):
      do_update(key, self.get_config_from_local_settings)

    do_set('SECRET_KEY', lambda(k): get_secret_key())
    do_update('{}_ENV'.format(self.app_name.upper()), '{}_prod'.format(self.app_name))
    do_update('NEW_RELIC_APP_NAME', self.app_name)
    if self.twitter_api:
      do_update_from_local_settings('TWITTER_APP_ID')
      do_update_from_local_settings('TWITTER_APP_SECRET')
      do_update_from_local_settings('TWITTER_APP_SECRET')
    do_update_from_local_settings('NEWRELIC_API_KEY')
    for name in self.extra_local_settings():
      do_update_from_local_settings(name)

  def update_buildpacks(self):
    execute('heroku buildpacks:clear')
    execute('heroku buildpacks:set heroku/python')
    for cmd in self.extra_buildpack_commands():
      execute(cmd)

  def extra_buildpack_commands(self):
    """Override to add any extra buildpacks."""
    return []

  def extra_local_settings(self):
    """Override to provide names of any other local settings that should be copied to prod."""
    return []

  def setup(self):
    self.update_heroku_config()
    self.update_buildpacks()


if __name__ == '__main__':
  SetupProd.create().setup()
