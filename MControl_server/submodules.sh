#!/bin/bash

git submodule update --init --recursive

# pip install -U pycrypto # <DEPRECATION>

# info:
#     PyCryptodome exposes almost the same API
#     as the old PyCrypto so that most
#     applications will run unmodified. 
pip install -U pycryptodome
# install package via setup.py (https://github.com/bssthu/pysqlsimplecipher.git)
pip install ./MControl_server/src/pysqlsimplecipher