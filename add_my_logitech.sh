#!/bin/bash

# the script below adds special mouse buttons on Logitech M546
# mouse wheel left click -> go backward, one page backward on browser
# mouse wheel right click -> go forward, one page foreward on browser
# back button near thumb -> volume down
# front button near thumb -> volume up

sudo apt install xdotool xbindkeys

xbindkeys --defaults > ~/.xbindkeysrc

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

xbindkeys -f ~/.xbindkeysrc
