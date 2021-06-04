#!/bin/bash

git submodule update --init --recursive
pip install -U pycrypto
pip install -U pysqlsimplecipher