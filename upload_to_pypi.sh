#!/bin/sh
# See http://peterdowns.com/posts/first-time-with-pypi.html
python setup.py register -r pypi
python setup.py sdist upload -r pypi
VERSION=`python setup.py -V`
VERSION_TAG="v${VERSION}"
git tag "${VERSION_TAG}"
git push origin "${VERSION_TAG}"
