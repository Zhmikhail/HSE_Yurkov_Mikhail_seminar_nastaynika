echo $PATH
export PATH=$PATH:$1
echo "export PATH=\$PATH:$1">>~/.zshrc


# Результат работы
# (base) zhmikhail@MacBook-Pro HSE_Yurkov_Mikhail_seminar_nastaynika % cat ~/.zshrc 

# # >>> conda initialize >>>
# # !! Contents within this block are managed by 'conda init' !!
# __conda_setup="$('/Users/zhmikhail/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
# if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
# else
#     if [ -f "/Users/zhmikhail/anaconda3/etc/profile.d/conda.sh" ]; then
#         . "/Users/zhmikhail/anaconda3/etc/profile.d/conda.sh"
#     else
#         export PATH="/Users/zhmikhail/anaconda3/bin:$PATH"
#     fi
# fi
# unset __conda_setup
# # <<< conda initialize <<<


# # The next line updates PATH for Yandex Cloud CLI.
# if [ -f '/Users/zhmikhail/yandex-cloud/path.bash.inc' ]; then source '/Users/zhmikhail/yandex-cloud/path.bash.inc'; fi

# # The next line enables shell command completion for yc.
# if [ -f '/Users/zhmikhail/yandex-cloud/completion.zsh.inc' ]; then source '/Users/zhmikhail/yandex-cloud/completion.zsh.inc'; fi

# export PATH=$PATH:/usr/local/clickhouse
# export MAVEN_HOME=$(which mvn)
# export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-14.0.1.jdk/Contents/Home
# eval "$(rbenv init - zsh)"

# plugins=(git zsh-autosuggestions)

# export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"
# (base) zhmikhail@MacBook-Pro HSE_Yurkov_Mikhail_seminar_nastaynika % cd hw2
# (base) zhmikhail@MacBook-Pro hw2 % sh 2.sh /ZOV
# /opt/homebrew/opt/postgresql@17/bin:/Users/zhmikhail/.rbenv/shims:/Users/zhmikhail/yandex-cloud/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/opt/local/bin:/opt/local/sbin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/local/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/bin:/var/run/com.apple.security.cryptexd/codex.system/bootstrap/usr/appleinternal/bin:/Library/Apple/usr/bin:/opt/homebrew/opt/postgresql@17/bin:/Users/zhmikhail/.rbenv/shims:/Users/zhmikhail/yandex-cloud/bin:/Users/zhmikhail/anaconda3/bin:/Users/zhmikhail/anaconda3/condabin:/usr/local/clickhouse:/Users/zhmikhail/.vscode/extensions/ms-python.debugpy-2025.14.1-darwin-arm64/bundled/scripts/noConfigScripts:/usr/local/clickhouse
# (base) zhmikhail@MacBook-Pro hw2 % cat ~/.zshrc

# # >>> conda initialize >>>
# # !! Contents within this block are managed by 'conda init' !!
# __conda_setup="$('/Users/zhmikhail/anaconda3/bin/conda' 'shell.zsh' 'hook' 2> /dev/null)"
# if [ $? -eq 0 ]; then
#     eval "$__conda_setup"
# else
#     if [ -f "/Users/zhmikhail/anaconda3/etc/profile.d/conda.sh" ]; then
#         . "/Users/zhmikhail/anaconda3/etc/profile.d/conda.sh"
#     else
#         export PATH="/Users/zhmikhail/anaconda3/bin:$PATH"
#     fi
# fi
# unset __conda_setup
# # <<< conda initialize <<<


# # The next line updates PATH for Yandex Cloud CLI.
# if [ -f '/Users/zhmikhail/yandex-cloud/path.bash.inc' ]; then source '/Users/zhmikhail/yandex-cloud/path.bash.inc'; fi

# # The next line enables shell command completion for yc.
# if [ -f '/Users/zhmikhail/yandex-cloud/completion.zsh.inc' ]; then source '/Users/zhmikhail/yandex-cloud/completion.zsh.inc'; fi

# export PATH=$PATH:/usr/local/clickhouse
# export MAVEN_HOME=$(which mvn)
# export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk-14.0.1.jdk/Contents/Home
# eval "$(rbenv init - zsh)"

# plugins=(git zsh-autosuggestions)

# export PATH="/opt/homebrew/opt/postgresql@17/bin:$PATH"
# export PATH=$PATH:/ZOV
# (base) zhmikhail@MacBook-Pro hw2 % 