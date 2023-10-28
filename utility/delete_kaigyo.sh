#!/bin/bash
##########################
## When you write it after the following command and execute it, it will become one line
## ls | while read l ; do echo command
##########################
\;>>work.log; done; perl -pi -e 's@\n@@g' work.log; cat work.log; rm work.log;
