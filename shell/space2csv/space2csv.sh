#!/bin/sh

cat ${1} | while read l;  do tr -s ' ' ',' > ${1}.csv; done

