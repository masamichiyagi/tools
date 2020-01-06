TOOLPATH='/data/tools/text_modify/'
#cp in/* out; IFS='@'; cat ${TOOLPATH}before_after.txt | while read b a ; do python ${TOOLPATH}bef_after.py -i out -o out -b $b -a $a ; done; IFS=
IFS='@'; cat ${TOOLPATH}before_after.txt | while read b a ; do python ${TOOLPATH}bef_after.py -i out -o out -b $b -a $a ; done; IFS=
