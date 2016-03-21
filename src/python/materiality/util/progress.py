# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

import sys
import threading

from colors import blue


class Progress(object):
  def __init__(self, current, goal, verb='Handled', plural_noun='Items'):
    self.lock = threading.Lock()
    self.current = current
    self.goal = goal
    self.verb = verb
    self.plural_noun = plural_noun

  def done(self):
    return self.current >= self.goal

  def increment(self, n=1):
    with self.lock:
      if self.current < self.goal:
        self.current += n
        sys.stderr.write(blue('\r{verb} {current}/{goal} {plural_noun}'.format(verb=self.verb,
                                                                               current=self.current,
                                                                               goal=self.goal,
                                                                               plural_noun=self.plural_noun)))
        if self.current >= self.goal:
          sys.stderr.write(b'\n')
