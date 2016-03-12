# coding=utf-8
# Copyright 2015 Materiality Labs.

from __future__ import (nested_scopes, generators, division, absolute_import, with_statement,
                        print_function, unicode_literals)

from colors import green, blue

from materiality.util.execute import execute, get_output


default_dumpfile_path = './latest.dump'


def do_dump():
  print(green('Dumping production database: '))
  url = get_output('heroku pg:backups public-url')
  print(green('Database dump available at ' + blue(url)))

  print(green('Fetching dumpfile: '))
  execute('curl -o {0} {1}'.format(default_dumpfile_path, url))
  print(green('Production database dump written to {0}'.format(default_dumpfile_path)))

  print(green('Run ') + blue('./nuke_db.sh') + green(' to delete your existing local database, '))
  print(green('and ') + blue('./setup_dev.sh') + green(' to create a new one based on the dumped data.'))
  #print(green('Then run ') + blue('./sync_images_from_production.sh') + green(' to fetch production images.'))


if __name__ == '__main__':
  do_dump()
