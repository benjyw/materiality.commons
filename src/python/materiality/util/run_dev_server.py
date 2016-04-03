# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import argparse
import socket

from colors import blue, green, red

from materiality.util.execute import execute, execute_postgres


def run_dev_server(args):
  print(green('Starting local postgres server.'))
  execute_postgres('start')
  try:
    print(green('\nStarting local webapp.'))
    cmd = './venv/bin/python manage.py runserver'
    if args.insecure:
      cmd += ' --insecure'
    if args.with_remote_access:
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


def main():
  parser = argparse.ArgumentParser(description='Run a dev server for a materiality-based app.')
  parser.add_argument('--with-remote-access', action='store_true',
                      help='Allow non-localhost access (e.g., for testing from a mobile device).')
  parser.add_argument('--insecure', action='store_true',
                      help='Allow insecure access (e.g., for serving static files while testing with DEBUG=False).')
  args = parser.parse_args()
  run_dev_server(args)


if __name__ == '__main__':
  main()
