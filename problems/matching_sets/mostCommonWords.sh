#!/bin/sh

file=$1

cat $file \
  | tr ' ' '\n' \
  | tr 'A-Z' 'a-z' \
  | sed 's/[^a-z]//g' \
  | egrep -v '^\s*$' \
  | egrep -v '^(a|about|after|also|an|and|are|as|at|be|by|can|come|could|do|for|from|get|give|has|have|how|if|in|into|is|it|its|just|like)$' \
  | egrep -v '^(make|no|of|on|or|other|out|over|say|see|so|such|take|than|that|the|their|them|then|they|this|to)$' \
  | egrep -v '^(up|use|want|was|well|what|when|which|who|will|with|work|would|you|your)$' \
  | sort \
  | uniq -c \
  | sort -n \
  | tail -n 50

