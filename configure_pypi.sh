#!/bin/bash

if [ -z $1 ] || [ -z $2 ]; then
    echo "Missing arguments. ./configure-pypi <username> <password>"
    exit 1
fi

if [ -e ~/.pypirc ]; then
    echo "~/.pypirc would be overwritten. Quiting."
    exit 1
fi

cat << EOF > ~/.pypirc
[distutils]
index-servers =
    pypi

[pypi]
repository: https://pypi.python.org/pypi
username: $1
password: $2
EOF
