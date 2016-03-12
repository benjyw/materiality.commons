# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os
import shutil

from colors import green, blue

from materiality.util.prompt import confirm


def nuke_db():
  if confirm('This will destroy all the data in your local database. Are you sure?'):
    pgsql_dir = './pgsql'
    if os.path.exists(pgsql_dir):
      shutil.rmtree(pgsql_dir)
    print(green('Local database nuked. Run ') + blue('./setup_dev.sh') + green(' to create a new one.'))


if __name__ == '__main__':
  nuke_db()
