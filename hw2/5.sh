sleep 10& sleep 20& sleep 30& 

# Задача не совсем на баш в файле, делал ее в терминале
# (base) zhmikhail@MacBook-Pro hw2 % sleep 100&
# sleep 200&
# sleep 300&
# jobs
# [1] 97779
# [2] 97780
# [3] 97781
# [1]    running    sleep 100
# [2]  - running    sleep 200
# [3]  + running    sleep 300
# (base) zhmikhail@MacBook-Pro hw2 % fg %3
# [3]  - running    sleep 300
# ^C
# (base) zhmikhail@MacBook-Pro hw2 % jobs
# [2]  + running    sleep 200
# (base) zhmikhail@MacBook-Pro hw2 % fg %2
# [2]  + running    sleep 200
# ^C
# (base) zhmikhail@MacBook-Pro hw2 % jobs 
# (base) zhmikhail@MacBook-Pro hw2 % jobs
