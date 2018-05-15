# User dependent .bashrc file

# If not running interactively, don't do anything
[[ "$-" != *i* ]] && return

#
# Interactive operation...
# alias rm='rm -i'
# alias cp='cp -i'
# alias mv='mv -i'
#
# Default to human readable figures
alias df='df -h'
alias du='du -h'
#
# Misc :)
# alias less='less -r'                          # raw control characters
# alias whence='type -a'                        # where, of a sort
alias grep='grep --color'                     # show differences in colour
alias egrep='egrep --color=auto'              # show differences in colour
alias fgrep='fgrep --color=auto'              # show differences in colour
#
# Some shortcuts for different directory listings
# alias ls='ls -hF --color=tty'                 # classify files in colour
# alias dir='ls --color=auto --format=vertical'
# alias vdir='ls --color=auto --format=long'
alias ll='ls -l'                              # long list
alias la='ls -A'                              # all but . and ..
alias l='ls -CF'                              #

alias docs='cd /c/code/Documentation'
alias agent='cd /c/code/SnowInventoryAgent'
alias unix-agent='cd /c/code/unix_agent'
string="$(uname -a)"
if [[ $string == *"CYGWIN"* ]]; then
	alias generate-64='cmake -G "Visual Studio 12 2013 Win64" -DCMAKE_GENERATOR_TOOLSET=v120_xp -DCMAKE_BUILD_TYPE=Debug ..'
	alias generate-32='cmake -G "Visual Studio 12 2013" -DCMAKE_BUILD_TYPE=Debug -DCMAKE_GENERATOR_TOOLSET=v120_xp ..'
	alias build='cmake --build . --config Debug'
else
	alias generate='cmake -DCMAKE_BUILD_TYPE=Debug ..'
	alias build='make -j8'
fi
