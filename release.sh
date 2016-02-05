#!/bin/bash

VERSION=$1

sed  s/{{VERSION}}/$VERSION/ setup.tmpl.py > setup.py

python setup.py sdist bdist_wheel upload
