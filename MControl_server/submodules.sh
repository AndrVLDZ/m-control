#!/bin/bash

git submodule update --init --recursive

# pip install -U pycrypto # <DEPRECATION>

# info:
#     PyCryptodome exposes almost the same API
#     as the old PyCrypto so that most
#     applications will run unmodified. 
pip install -U pycryptodome
pip install -U pysqlsimplecipher