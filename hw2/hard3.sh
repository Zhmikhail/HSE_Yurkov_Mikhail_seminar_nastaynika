mkdir -p $1/Images $1/Documents;for f in $1/*;do case "${f##*.}" in jpg|png|gif) mv "$f" $1/Images/>>sort.log 2>&1;; txt|pdf|docx) mv "$f" $1/Documents/>>sort.log 2>&1;; esac;done;echo "$(date): Sorting completed">>sort.log

# Результат 
# Все файлы перемещены по крону. Крон сделал так
# 0 23 * * * /bin/bash /path/to/sort.sh /path/to/directory >> /path/to/sort.log 2>&1
# лог в файле 
# sort.log
