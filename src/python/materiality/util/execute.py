# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import shlex
import subprocess

"""Basic process execution functionality.

Note: No third-party deps, so we can use this in verify_venv.py.
"""

local_pgsql_dir = './pgsql/data'
local_pgsql_logfile = './pgsql/logfile'


def _munge_cmd(cmd):
  if isinstance(cmd, (str, unicode)):
    args = shlex.split(cmd)
  else:
    args = cmd
  return args


def execute(cmd):
  subprocess.check_call(_munge_cmd(cmd))


def get_output(cmd):
  return subprocess.check_output(_munge_cmd(cmd))


def execute_postgres(cmd):
  execute('pg_ctl -D {0} -l {1} {2}'.format(local_pgsql_dir, local_pgsql_logfile, cmd))
