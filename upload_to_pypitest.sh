#!/bin/sh
# See http://peterdowns.com/posts/first-time-with-pypi.html
python setup.py register -r pypitest
python setup.py sdist upload -r pypitest
