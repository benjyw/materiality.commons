# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from datetime import datetime

from colors import blue, green, red
import requests

from materiality.util.django_settings import get_django_settings
from materiality.util.execute import execute, get_output
from materiality.util.prompt import confirm


class Deployer(object):
  @staticmethod
  def check_for_master_branch():
    current_branch = get_output('git rev-parse --abbrev-ref HEAD').strip()
    return current_branch == 'master'

  @staticmethod
  def check_for_clean_workspace():
    return get_output('git status --porcelain').strip() == ''

  @staticmethod
  def check_for_unpushed_commits():
    revs = get_output('git rev-list --left-right origin/master...HEAD').splitlines()
    local_only_commits = [rev for rev in revs if rev.startswith('>')]
    return local_only_commits == []

  @staticmethod
  def get_changed_files():
    return set([s[3:].strip() for s in get_output('git status --porcelain').splitlines()])

  def __init__(self, app_name):
    self._app_name = app_name.lower()

  def compile_js(self):
    raise NotImplementedError('Subclasses must implement.')

  def log_to_newrelic(self, tag):
    # Log to New Relic that we've deployed, so they can mark it in the graphs.
    url = 'https://api.newrelic.com/deployments.xml'
    headers = {'x-api-key': get_django_settings().NEWRELIC_API_KEY}
    data = {
      'deployment[app_name]': self._app_name,
      'deployment[description]': tag
    }
    r = requests.post(url, headers=headers, data=data)
    r.raise_for_status()

  def deploy(self):
    if not self.check_for_master_branch():
      print(red('Not on master branch! Aborted.'))
      return

    if not self.check_for_clean_workspace():
      print(red('Workspace is not clean! Aborted.'))
      return

    if not self.check_for_unpushed_commits():
      print(red('You have unpushed local commits! Aborted.'))
      return

    tag = '{}_release_{}'.format(self._app_name, datetime.now().strftime('%Y%m%d_%H%M%S'))
    print(green('Creating release {}'.format(blue(tag))))

    print(green('Building JavaScript bundles.'))
    modified_prod_js_files = self.compile_js()

    if modified_prod_js_files:
      print(green('Committing new minimized JavaScript to master.'))
      for path in modified_prod_js_files:
        execute('git add {}'.format(path))
      execute('git commit -m "Minimized JS for release {}."'.format(tag))
    else:
      print(green('Minimized JavaScript unchanged.'))

    print('')
    print(green('Last chance test this release!'))

    print('')
    if confirm('OK to push to github?'):
      execute('git push origin master')
      print('')
      if confirm('OK to deploy?'):
        execute('git tag -a {tag} -m "Tag for release {tag}."'.format(tag=tag))
        execute('git push --tags origin')
        execute('git push heroku master')
        self.log_to_newrelic(tag)
      else:
        print('')
        print(red('Aborted!'))
    else:
      print('')
      print(red('Aborted!'))


  if __name__ == '__main__':
    deploy()
