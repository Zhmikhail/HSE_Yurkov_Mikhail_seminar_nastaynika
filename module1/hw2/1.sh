for f in *;do [ "$f" = "$1" ]&&echo "Found: $f"||echo "$f: $(ls -ld "$f"|cut -d' ' -f1)";done


# Пример работы:
# (base) zhmikhail@MacBook-Pro hw2 % sh 1.sh     
# 1.sh: -rw-r--r--
# 2.sh: -rw-r--r--
# 3.sh: -rw-r--r--
# (base) zhmikhail@MacBook-Pro hw2 % sh 1.sh 2.sh
# 1.sh: -rw-r--r--
# Found: 2.sh
# 3.sh: -rw-r--r--
# (base) zhmikhail@MacBook-Pro hw2 % sh 1.sh 0.sh
# 1.sh: -rw-r--r--
# 2.sh: -rw-r--r--
# 3.sh: -rw-r--r--
# (base) zhmikhail@MacBook-Pro hw2 % 
