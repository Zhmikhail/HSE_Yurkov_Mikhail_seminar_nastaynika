d=$(date +%Y-%m-%d);for f in $1/*;do [[ "$f" != *backup.log && "$f" != *_20*-*-* ]]&&cp "$f" "${f}_$d";done;c=$(ls $1/*_$d 2>/dev/null|wc -l);echo "$(date): Backed up $c files">>$1/backup.log;echo "Done: $c files"

# результат работы в папке test_backup (бэкап собирается, файлы бэкапа и лога не бэкапируются)