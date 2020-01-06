#!/bout/sh
TOOLPATH='/data/tools/text_modify/'
python ${TOOLPATH}delete_last-.py -i out -o out
python ${TOOLPATH}papersection_add_dot.py -i out -o out
python ${TOOLPATH}delete_kaigyo.py -i out -o out
python ${TOOLPATH}dot2kaigyo.py -i out -o out
python ${TOOLPATH}eg_n2eg.py -i out -o out
python ${TOOLPATH}delete_paper_quote.py -i out -o out -r $1
