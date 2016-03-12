# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from collections import OrderedDict
import os
import textwrap
import time

import sys
from colors import green, red, blue
import psycopg2

from materiality.util.dump_production_database import default_dumpfile_path
from materiality.util.execute import execute, execute_postgres, local_pgsql_dir
from materiality.util.fileutil import backup, umask
from materiality.util.prompt import confirm, get_database_password, get_secret_key


_local_settings_file = 'main/settings_local.py'


class SetupDev(object):
  @staticmethod
  def get_twitter_app_id():
    return raw_input(green('Paste Twitter app id: '))

  @staticmethod
  def get_twitter_app_secret():
    return raw_input(green('Paste Twitter app secret: '))

  @staticmethod
  def get_newrelic_api_key():
    return raw_input(green('Paste NewRelic API key: '))

  @staticmethod
  def sync_database():
    print(green('Syncing database:'))
    execute('./venv/bin/python manage.py migrate')
    print('')

  @classmethod
  def create_or_update_local_settings(cls):
    print(green('\nVerifying local settings file.'))
    if os.path.exists(_local_settings_file):
      existing_settings = {}
      execfile(_local_settings_file, existing_settings)
      print(green('Found local settings file. Updating it.'))
    else:
      existing_settings = {}
      print(green('No local settings file. Creating one.'))

    updated_settings = OrderedDict()
    def update_setting(name, func):
      if name in existing_settings:
        updated_settings[name] = existing_settings[name]
      else:
        updated_settings[name] = func()

    update_setting('SECRET_KEY', get_secret_key)
    update_setting('DEFAULT_DATABASE_PASSWORD', get_database_password)
    update_setting('TWITTER_APP_ID', cls.get_twitter_app_id)
    update_setting('TWITTER_APP_SECRET', cls.get_twitter_app_secret)
    update_setting('NEWRELIC_API_KEY', cls.get_newrelic_api_key)

    with backup(_local_settings_file) as bak:
      with umask(0):
        with os.fdopen(os.open(_local_settings_file, os.O_WRONLY | os.O_CREAT, 0o400), 'w') as outfile:
          outfile.write(textwrap.dedent("""
          # coding=utf-8
          # Copyright 2015 Materiality Labs.

          from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                                  print_function, unicode_literals)


          """).lstrip())
          outfile.write(b"# SECURITY WARNING: keep everything in this file secret!\n\n")
          for key, val in updated_settings.items():
            outfile.write("{0} = '{1}'\n".format(key, val))

    os.unlink(bak)
    print(green('Wrote {0}.\n'.format(_local_settings_file)))
    return updated_settings

  @classmethod
  def execute_sql(cls, sql):
    try:
      with psycopg2.connect("dbname='postgres' host='localhost'") as conn:
        conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()
        cur.execute(sql)
    except psycopg2.Error as e:
      print('ERROR: %s' % e)
      return False
    return True

  def __init__(self, app_name):
    self._app_name = app_name.lower()

  @property
  def db_name(self):
    return self._app_name  # Name the db after the app, for simplicity.

  @property
  def db_user(self):
    return self._app_name  # Name the user after the app, for simplicity.

  def setup_postgres(self, default_pwd):
    print(green('Verifying local postgres database.'))
    if os.path.exists(local_pgsql_dir):
      print(green('Local postgres database exists.'))
    elif confirm('Set up local postgress database? (only do this on dev machines)'):
      print(blue('Initializing database cluster.'))
      execute_postgres('initdb')

      print(blue('Starting database server.'))
      execute_postgres('start')

      try:
        print(blue('Waiting for database server to start.'))
        time.sleep(1.0)
        attempts = 0
        max_attempts = 10
        while True:
          attempts += 1
          if self.execute_sql('SELECT 1'):
            break
          if attempts < max_attempts:
            time.sleep(1.0)
          else:
            raise Exception('Failed to connect to database server.')
        print(blue('Database server started.'))

        print(blue('Creating database.'))
        if not self.execute_sql('CREATE DATABASE {}'.format(self.db_name)):
          raise Exception('Failed to create database.')

        print(blue('Creating database user.'))
        if not self.execute_sql("CREATE ROLE {0} PASSWORD '{1}' LOGIN".format(self.db_user, default_pwd)):
          raise Exception('Failed to create role.')

        print(blue('Creating database user permissions.'))
        if not self.execute_sql('GRANT ALL ON DATABASE {0} to {1}'.format(self.db_name, self.db_user)):
          raise Exception('Failed to create role.')

        if os.path.exists(default_dumpfile_path) and confirm('Detected dumpfile at {0}. Import data from it?'.format(default_dumpfile_path)):
          self.import_database_dump(default_dumpfile_path)
        else:
          self.sync_database()

      except Exception as e:
        print(red('ERROR: %s' % e))
        raise
      finally:
        print(blue('Stopping database server.'))
        execute_postgres('stop')

      print(green('Set up local postgres database at {0}.'.format(local_pgsql_dir)))

  def import_database_dump(self, dumpfile):
    print(green('Importing data from {0}:'.format(dumpfile)))
    execute('pg_restore --verbose --no-acl --no-owner -n public -h localhost -U {0} -d {1} {2}'.format(self.db_user, self.db_name, dumpfile))
    print('')

  def setup(self):
    settings = self.create_or_update_local_settings()
    self.setup_postgres(settings['DEFAULT_DATABASE_PASSWORD'])
    print(green('Done!'))


if __name__ == '__main__':
  if len(sys.argv) != 2:
    raise Exception('Expected exactly one cmd-line arg, specifying the app name.')
  SetupDev(sys.argv[1]).setup()
