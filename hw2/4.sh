h(){ echo "Hello, $1";};
s(){ echo $(($1+$2));};
h "World";s 5 3

# Результат работы 
# sh 4.sh       
# Hello, World
# 8
