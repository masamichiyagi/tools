IFS='@'; cat before_after.txt | while read b a ; do python /data/tools/text_modify/bef_after.py -i in -o in -b $b -a $a ; done; IFS=
