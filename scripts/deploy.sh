#!/bin/bash

# will fail if you do not increment the version
# number in setup.py

rm -rf dist
python3 setup.py sdist bdist_wheel
twine upload dist/*