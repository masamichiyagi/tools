#!/bin/sh

cat ${1} | while read l;  do tr -s ' ' '\t' > ${1}.csv; done

