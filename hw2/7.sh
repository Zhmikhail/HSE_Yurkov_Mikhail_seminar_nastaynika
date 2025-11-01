echo "alias ll='ls -la'">>~/.zshrc

echo '
autoload -Uz add-zsh-hook

my_cd_hook() {
  if [[ $BUFFER == "cd /T"* || $BUFFER == "cd /Т"* ]]; then
    BUFFER='cd "/Ти-ти-ти-та/тири-тёуто!/Тиииииииии-та/рири-тёу!/Тити-рити/Ри-ти,/ти-ритёу,/Тити-утя/утя/Ри-ти-Тёу!"'
    zle end-of-line
  fi
  zle redisplay
}

zle -N my_cd_hook

bindkey '^I' my_cd_hook
' >> ~/.zshrc


# Результат работы 
# Алиас работает
# (base) zhmikhail@MacBook-Pro hw2 % ll              
# total 80
# drwxr-xr-x  12 zhmikhail  staff   384 Nov  1 22:32 .
# drwxr-xr-x   8 zhmikhail  staff   256 Nov  1 11:25 ..
# -rw-r--r--   1 zhmikhail  staff   479 Nov  1 11:27 1.sh
# -rw-r--r--   1 zhmikhail  staff  3586 Nov  1 22:02 2.sh
# -rw-r--r--   1 zhmikhail  staff   471 Nov  1 22:24 3.sh
# -rw-r--r--   1 zhmikhail  staff   137 Nov  1 22:28 4.sh
# -rw-r--r--   1 zhmikhail  staff   650 Nov  1 22:48 5.sh
# -rw-r--r--   1 zhmikhail  staff   271 Nov  1 22:35 6.sh
# -rw-r--r--   1 zhmikhail  staff   100 Nov  1 22:35 7.sh
# -rw-r--r--   1 zhmikhail  staff    38 Nov  1 22:33 error.log
# -rw-r--r--   1 zhmikhail  staff    10 Nov  1 22:32 input.txt
# -rw-r--r--   1 zhmikhail  staff     9 Nov  1 22:33 output.txt
# Команда дополняется при написании cd /T{TAB}
# cd /Tmy_cd_hook:2: no such file or directory: /Ти-ти-ти-та/тири-тёуто!/Тиииииииии-та/рири-тёу!/Тити-рити/Ри-ти,/ти-ритёу,/Тити-утя/утя/Ри-ти-Тёу!
# (base) zhmikhail@MacBook-Pro ~ % cd /T
# Из минусов - дефолт автодополнение ломается