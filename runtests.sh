#!/bin/bash
python3 freetests.py
V=$?
[ $V == 0 ] && echo "Tests PASSED!" && exit
echo "Tests did not pass :("
