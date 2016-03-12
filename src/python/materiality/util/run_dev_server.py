# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import socket
import sys

from colors import blue, green, red

from materiality.util.execute import execute, execute_postgres


def run_dev_server():
  print(green('Starting local postgres server.'))
  execute_postgres('start')
  try:
    print(green('\nStarting local webapp.'))
    cmd = './venv/bin/python manage.py runserver'
    if with_remote_access:
      cmd += ' 0.0.0.0:8000'
      my_host = socket.gethostbyname(socket.gethostname())
      print(blue('\nAccess remotely at http://{0}:8000'.format(my_host)))
    execute(cmd)  # Run directly.
    #execute('heroku local')  # Run via local heroku setup.  Must run `source venv/bin/activate` first!
  except Exception:
    print(red('\nEncountered error!'))
    raise
  finally:
    print(green('\nStopping local postgres server.'))
    execute_postgres('stop')

  print('\n')


if __name__ == '__main__':
  with_remote_access = False
  if len(sys.argv) > 1:
    if len(sys.argv) == 2 and sys.argv[1] == '--with-remote-access':
      with_remote_access = True
    else:
      print(red('Unknown options: {0}'.format(' '.join(sys.argv[1:]))))
      sys.exit(1)
  run_dev_server()
