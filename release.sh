#!/bin/bash

VERSION=$1

sed  s/{{VERSION}}/$VERSION/ setup.py.tmpl > setup.py

python setup.py sdist upload
