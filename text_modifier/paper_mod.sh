#!/bin/sh
python delete_last-.py -i in -o in
python papersection_add_dot.py -i in -o in
python delete_kaigyo.py -i in -o in
python dot2kaigyo.py -i in -o in
python eg_n2eg.py -i in -o in
python delete_paper_quote.py -i in -o out -r $1
