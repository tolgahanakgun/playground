#!/bin/bash

# install required libraries
apt install xdotool xbindkeys

# add default keybindings to file
xbindkeys --defaults > ~/.xbindkeysrc

# add Logitech M546 key bindings
cat <<EOT >> ~/.xbindkeysrc
"xdotool key XF86Back"
    b:6
"xdotool key XF86Forward"
    b:7
"xdotool keydown XF86AudioLowerVolume"
    b:8
"xdotool keyup XF86AudioLowerVolume"
    b:8 + Release
"xdotool keydown XF86AudioRaiseVolume"
    b:9
"xdotool keyup XF86AudioRaiseVolume"
    b:9 + Release
EOT
