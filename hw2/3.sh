read n
[ $n -gt 0 ]&&echo positive||([ $n -lt 0 ]&&echo negative||echo zero)
[ $n -gt 0 ] && (i=1; while [ $i -le $n ]; do echo $i; i=$((i+1)); done) || echo 'not while'

# Результат работы 
# (base) zhmikhail@MacBook-Pro hw2 % sh 3.sh 
# 6
# positive
# 1
# 2
# 3
# 4
# 5
# 6
# (base) zhmikhail@MacBook-Pro hw2 % sh 3.sh 
# 0
# zero
# not while
# (base) zhmikhail@MacBook-Pro hw2 % sh 3.sh 
# -6
# negative
# not while
# (base) zhmikhail@MacBook-Pro hw2 % 