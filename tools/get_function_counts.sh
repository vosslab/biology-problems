#!/bin/bash

for func in $(grep -E '^def [a-z]' bptools.py | cut -c5- | gsed 's/(.*$//');
do
  count=$(grep -h -F -- "${func}(" $(find problems/ -name "*.py" -type f) | wc -l);
  echo "$count $func";
done | sort -n
