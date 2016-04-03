# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from contextlib import contextmanager

from pympler import muppy, summary


@contextmanager
def print_memory_summary():
  sum1 = summary.summarize(muppy.get_objects())
  yield
  sum2 = summary.summarize(muppy.get_objects())
  diff = summary.get_diff(sum1, sum2)
  summary.print_(diff)
