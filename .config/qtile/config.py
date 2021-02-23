# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import re
import socket
import subprocess
from libqtile.config import KeyChord, Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget, hook
from libqtile.lazy import lazy
from typing import List  # noqa: F401

mod = "mod4"
myTerm = "alacritty"
myConfig = "/home/beron/.config/qtile/config.py"

keys = [
    # Switch between windows in current stack pane
    Key([mod], "k", 
        lazy.layout.down(),
        desc="Move focus down in stack pane"
    ),
    Key([mod], "j", lazy.layout.up(),
        desc="Move focus up in stack pane"
    ),
    # Move windows up or down in current stack
    Key([mod, "control"], "k", 
        lazy.layout.shuffle_down(),
        desc="Move window down in current stack "
    ),
    Key([mod, "control"], "j", 
        lazy.layout.shuffle_up(),
        desc="Move window up in current stack "
    ),
    # Switch window focus to other pane(s) of stack
    Key([mod], "space", 
        lazy.layout.next(),
        desc="Switch window focus to other pane(s) of stack"
    ),
    # Swap panes of split stack
    Key([mod, "shift"], "space", 
        lazy.layout.rotate(),
        desc="Swap panes of split stack"
    ),
### Dmenu scripts launched with ALT + CTRL + KEY
    Key(["mod1", "control"], "e",
        lazy.spawn("./.dmenu/dmenu-edit-configs.sh"),
        desc='Dmenu script for editing config files'
    ),
    Key(["mod1", "control"], "m",
        lazy.spawn("./.dmenu/dmenu-sysmon.sh"),
        desc='Dmenu system monitor script'
    ),
    Key(["mod1", "control"], "p",
        lazy.spawn("passmenu"),
        desc='Passmenu'
    ),
    Key(["mod1", "control"], "r",
        lazy.spawn("dmenu_run"),
        desc='Dmenu reddio script'
    ),
    Key(["mod1", "control"], "s",
        lazy.spawn("./.dmenu/dmenu-surfraw.sh"),
        desc='Dmenu surfraw script'
    ),
    Key(["mod1", "control"], "t",
        lazy.spawn("./.dmenu/dmenu-trading.sh"),
        desc='Dmenu trading programs script'
    ),
    Key(["mod1", "control"], "i",
        lazy.spawn("./.dmenu/dmenu-scrot.sh"),
        desc='Dmenu scrot script'
    ),
    Key(["mod1", "control"], "b",
        lazy.spawn("qutebrowser"),
        desc='Open qutebrowser'
    ),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key([mod, "shift"], "Return", 
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack"
    ),
    Key([mod], "Return", 
        lazy.spawn(myTerm), 
        desc="Launch terminal"
    ),
    # Toggle between different layouts as defined below
    Key([mod], "Tab", 
        lazy.next_layout(), 
        desc="Toggle between layouts"
    ),
    Key([mod], "w", 
        lazy.window.kill(), 
        desc="Kill focused window"
    ),

    Key([mod, "control"], "r", 
       lazy.restart(), 
       desc="Restart qtile"
    ),
    Key([mod, "control"], "q", 
        lazy.shutdown(),
        desc="Shutdown qtile"
    ),
    Key([mod], "r", lazy.spawncmd(),
        desc="Spawn a command using a prompt widget"
    ),
# Also allow changing volume the old fashioned way.
    Key([mod], "plus", lazy.spawn("amixer -c 0 -q set Master 2dB+")),
    Key([mod], "minus", lazy.spawn("amixer -c 0 -q set Master 2dB-")),
]

group_names = [("WWW", {'layout': 'max'}),  
               ("DEV", {'layout': 'monadtall'}),  
               ("SYS", {'layout': 'monadtall'}),  
               ("DOC", {'layout': 'monadtall'}),
               ("GFX", {'layout': 'floating'})]

groups = [Group(name,**kwargs) for name, kwargs in group_names]

for i, (name, kwargs) in enumerate(group_names, 1):
    keys.append(Key([mod], str(i), lazy.group[name].toscreen()))           # Switch to another group
    keys.append(Key([mod, "shift"], str(i), lazy.window.togroup(name)))   # Send current window to another group

layout_theme = {"border_width": 3,
                "margin": 3,
                "border_focus": "1DF77D",
                "border_normal": "218359"
                }


layouts = [
    #layout.MonadWide(**layout_theme),
    #layout.Bsp(**layout_theme),
    #layout.Stack(stacks=2, **layout_theme),
    #layout.Columns(**layout_theme),
    #layout.RatioTile(**layout_theme),
    #layout.VerticalTile(**layout_theme),
    #layout.Matrix(**layout_theme),
    #layout.Zoomy(**layout_theme),
    layout.MonadTall(**layout_theme),
    layout.Max(**layout_theme),
    layout.Tile(shift_windows=True, **layout_theme),
    layout.Stack(num_stacks=2),
    layout.TreeTab(
        font = "Anonymous Pro Minus",
        fontsize = 10,
        sections = ["FIRST", "SECOND"],
        section_fontsize = 11,
        bg_color = "141414",
        active_bg = "90C435",
        active_fg = "000000",
        inactive_bg = "384323",
        inactive_fg = "a0a0a0",
        padding_y = 5,
        section_top = 10,
        panel_width = 320
        ),
        layout.Floating(**layout_theme)
]

colors = [["#333333", "#333333"], # panel background
          ["#5e5c5d", "#5e5c5d"], # background for current screen tab
          ["#ffffff", "#ffffff"], # font color for group names
          ["#1DF77D", "#1DF77D"], # border line color for current tab
          ["#3DB188", "#3DB188"], # border line color for other tab and odd widgets
          ["#4E93D4", "#4E93D4"], # color for the even widgets
          ["#48F5D4", "#48F5D4"]] # window name

prompt = "{0}@{1}: ".format(os.environ["USER"], socket.gethostname())

##### DEFAULT WIDGET SETTINGS #####
widget_defaults = dict(
    font = "Jetbrains Mono",
    fontsize = 12,
    padding = 2,
    background=colors[0]
)
extension_defaults = widget_defaults.copy()

def init_widgets_list():
    widgets_list = [
                       
            widget.Sep(
                       linewidth = 0,
                       padding = 6,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.GroupBox(
                       font = "Jetbrains Mono",
                       fontsize = 14,
                       margin_y = 4,
                       margin_x = 3,
                       padding_y = 3,
                       padding_x = 3,
                       borderwidth = 3,
                       active = colors[2],
                       inactive = colors[2],
                       rounded = True,
                       highlight_color = colors[1],
                       highlight_method = "line",
                       this_current_screen_border = colors[3],
                       this_screen_border = colors [4],
                       other_current_screen_border = colors[0],
                       other_screen_border = colors[0],
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.Prompt(
                       prompt = prompt,
                       font = "Jetbrains Mono",
                       padding = 12,
                       foreground = colors[3],
                       background = colors[1]
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 40,
                       foreground = colors[2],
                       background = colors[0]
                       ),
              widget.WindowName(
                       foreground = colors[6],
                       background = colors[0],
                       padding = 0
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[0],
                       foreground = colors[4],
                       padding = -6,
                       fontsize = 60
                       ),
              widget.TextBox(
                       text = " ⟳ ",
                       padding = 2,
                       foreground = colors[2],
                       background = colors[4],
                       fontsize = 20
                       ),
              widget.Pacman(
                       update_interval = 1800,
                       foreground = colors[2],
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       background = colors[4]
                       ),
              widget.TextBox(
                       text = "Updates",
                       padding = 5,
                       mouse_callbacks = {'Button1': lambda qtile: qtile.cmd_spawn(myTerm + ' -e sudo pacman -Syu')},
                       foreground = colors[2],
                       background = colors[4]
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -6,
                       fontsize = 60
                       ),
             # widget.Net(
             #          interface = "enp1s0f2",
             #          format = '{down} ↓↑ {up}',
             #          foreground = colors[2],
             #          background = colors[5],
             #          padding = 10
             #          ),
              widget.Net(
                       interface = "wlp2s0",
                       format = '{down} ↓↑ {up}',
                       foreground = colors[2],
                       background = colors[5],
                       padding = 10
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[5],
                       foreground = colors[4],
                       padding = -6,
                       fontsize = 60
                       ),
              widget.TextBox(
                      text = " Vol:",
                       foreground = colors[2],
                       background = colors[4],
                       padding = 0
                       ),
              widget.Volume(
                       foreground = colors[2],
                       background = colors[4],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[4],
                       foreground = colors[5],
                       padding = -6,
                       fontsize = 60
                       ),
              widget.CurrentLayoutIcon(
                       custom_icon_paths = [os.path.expanduser("~/.config/qtile/icons")],
                       foreground = colors[0],
                       background = colors[5],
                       padding = 0,
                       scale = 0.7
                       ),
              widget.CurrentLayout(
                       foreground = colors[2],
                       background = colors[5],
                       padding = 5
                       ),
              widget.TextBox(
                       text = '',
                       background = colors[5],
                       foreground = colors[4],
                       padding = -6,
                       fontsize = 60
                       ),
              widget.TextBox(
                      text = '  ',
                      background = colors[4],
                      foreground= colors[2],
                      padding = 4,
                      fontsize = 20
                      ),
              widget.Clock(
                       padding = 4,
                       foreground = colors[2],
                       background = colors[4],
                       format = "%A, %B %d  [ %H:%M ]"
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 10,
                       foreground = colors[0],
                       background = colors[4]
                       ),
              widget.Systray(
                       background = colors[0],
                       padding = 10,
                       icons_size = 48
                       ),
              widget.Sep(
                       linewidth = 0,
                       padding = 10,
                       foreground = colors[2],
                       background = colors[0]
                       ),

    ]
    return widgets_list
def init_widgets_screen1():
    widgets_screen1 = init_widgets_list()
    return widgets_screen1

def init_screen():
    return[Screen(top=bar.Bar(widgets=init_widgets_screen1(), opacity=1.0, size=20))]

if __name__ in ["config", "__main_"]:
    screens = init_screen()
    widgets_list = init_widgets_list()
    widgets_screen1 = init_widgets_screen1()

# Drag floating layouts.
mouse = [
    Drag([mod], "Button1", lazy.window.set_position_floating(),
         start=lazy.window.get_position()),
    Drag([mod], "Button3", lazy.window.set_size_floating(),
         start=lazy.window.get_size()),
    Click([mod], "Button2", lazy.window.bring_to_front())
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: List
main = None  # WARNING: this is deprecated and will be removed soon
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False

floating_layout = layout.Floating(float_rules=[
    # Run the utility of `xprop` to see the wm class and name of an X client.
    {'wmclass': 'confirm'},
    {'wmclass': 'dialog'},
    {'wmclass': 'download'},
    {'wmclass': 'error'},
    {'wmclass': 'file_progress'},
    {'wmclass': 'notification'},
    {'wmclass': 'splash'},
    {'wmclass': 'toolbar'},
    {'wmclass': 'confirmreset'},  # gitk
    {'wmclass': 'makebranch'},  # gitk
    {'wmclass': 'maketag'},  # gitk
    {'wname': 'branchdialog'},  # gitk
    {'wname': 'pinentry'},  # GPG key password entry
    {'wmclass': 'ssh-askpass'},  # ssh-askpass
])
auto_fullscreen = True
focus_on_window_activation = "smart"

@hook.subscribe.startup_once
def start_once():
    home = os.path.expanduser('~')
    subprocess.call([home + '/.config/qtile/autostart.sh'])

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, GitHub issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"
