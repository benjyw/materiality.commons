# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import os
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


def _update_env(env):
  full_env = dict(os.environ)
  if env:
    full_env.update(env)
  return full_env

def execute(cmd, env=None):
  subprocess.check_call(_munge_cmd(cmd), env=_update_env(env))


def get_output(cmd, env=None):
  return subprocess.check_output(_munge_cmd(cmd), env=env)


def execute_postgres(cmd):
  execute('pg_ctl -D {0} -l {1} {2}'.format(local_pgsql_dir, local_pgsql_logfile, cmd))
