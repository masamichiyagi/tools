cp ./in/*.txt ./out/; IFS='@'; cat /data/tools/text_modify/mail_befaf.txt | while read b a ; do python /data/tools/text_modify/bef_after.py -i out -o out -b $b -a $a ; done; IFS=
