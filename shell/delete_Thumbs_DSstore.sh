#!/bin/sh

#find . -name 'Thumbs.db' -exec rm -rf {} \;
find . -name '.ipynb_checkpoints' -exec rm -rf {} \;
find . -name '~$*' -exec rm -rf {} \;
find . -name '.DS_Store' -exec rm -rf {} \;

