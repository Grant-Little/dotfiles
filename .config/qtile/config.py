from libqtile import bar, layout, qtile, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile import hook

import os
import subprocess
import random

from dataclasses import dataclass

home = os.path.expanduser('~')

@dataclass
class Colors:
    black: str
    grey: str
    red: str
    green: str
    yellow: str
    blue: str
    magenta: str
    cyan: str
    white: str

@dataclass
class Theme:
    border_width: int
    gap_width: int
    bar_size: int
    colors: Colors

monokai = Colors(
    "#272822",
    "#75715e",
    "#f92672",
    "#a6e22e",
    "#f4bf75",
    "#66d9ef",
    "#ae81ff",
    "#a1efe4",
    "#f8f8f2")

my_theme = Theme(2, 4, 25, monokai)

@hook.subscribe.startup_once
def autostart():
    subprocess.Popen(["picom", "--config", home + "/.config/picom/picom.conf"])

mod = "mod4"
terminal = "alacritty"

keys = [
    # Switch between windows
    Key(
        [mod],
        "h",
        lazy.layout.left(),
        desc="Move focus left"
    ),
    Key(
        [mod],
        "l",
        lazy.layout.right(),
        desc="Move focus right"
    ),
    Key(
        [mod],
        "j",
        lazy.layout.down(),
        desc="Move focus down"
    ),
    Key(
        [mod],
        "k",
        lazy.layout.up(),
        desc="Move focus up"
    ),
    Key(
        [mod],
        "tab",
        lazy.layout.next(),
        desc="Move window focus to other window"
    ),
    # Move windows between left/right columns or move up/down in current stack.
    # Moving out of range in Columns layout will create new column.
    Key(
        [mod, "shift"],
        "h",
        lazy.layout.shuffle_left(),
        desc="Move window to the left"
    ),
    Key(
        [mod, "shift"],
        "l",
        lazy.layout.shuffle_right(),
        desc="Move window to the right"
    ),
    Key(
        [mod, "shift"],
        "j",
        lazy.layout.shuffle_down(),
        desc="Move window down"
    ),
    Key(
        [mod, "shift"],
        "k",
        lazy.layout.shuffle_up(),
        desc="Move window up"
    ),
    # Grow windows. If current window is on the edge of screen and direction
    # will be to screen edge - window would shrink.
    Key(
        [mod, "control"],
        "h",
        lazy.layout.grow_left(),
        desc="Grow window left"
    ),
    Key(
        [mod, "control"],
        "l",
        lazy.layout.grow_right(),
        desc="Grow window right"
    ),
    Key(
        [mod, "control"],
        "j",
        lazy.layout.grow_down(),
        desc="Grow window down"
    ),
    Key(
        [mod, "control"],
        "k",
        lazy.layout.grow_up(),
        desc="Grow window up"
    ),
    Key(
        [mod],
        "n",
        lazy.layout.normalize(),
        desc="Reset all window sizes"
    ),
    # Toggle between split and unsplit sides of stack.
    # Split = all windows displayed
    # Unsplit = 1 window displayed, like Max layout, but still with
    # multiple stack panes
    Key(
        [mod, "shift"],
        "Return",
        lazy.layout.toggle_split(),
        desc="Toggle between split and unsplit sides of stack",
    ),
    Key(
        [mod],
        "Return",
        lazy.spawn(terminal),
        desc="Launch terminal"
    ),
    Key(
        [mod],
        "c",
        lazy.window.kill(),
        desc="Kill focused window"
    ),
    Key(
        [mod],
        "f",
        lazy.window.toggle_fullscreen(),
        desc="Toggle fullscreen on the focused window",
    ),
    Key(
        [mod],
        "space",
        lazy.window.toggle_floating(),
        desc="Toggle floating on the focused window"
    ),
    Key(
        [mod, "shift"],
        "r",
        lazy.reload_config(),
        desc="Reload the config"
    ),
    Key(
        [mod, "shift"],
        "e",
        lazy.shutdown(),
        desc="Shutdown Qtile"
    ),
    Key(
        [mod],
        "d",
        lazy.spawn("rofi -show drun"),
        desc="Launch Rofi as Dmenu"
    ),
    
    Key(
        [],
        "XF86AudioLowerVolume",
        lazy.spawn("amixer sset Master 5%-"),
        desc="Lower Volume"
    ),
    Key(
        [],
        "XF86AudioRaiseVolume",
        lazy.spawn("amixer sset Master 5%+"),
        desc="Raise Volume"
    ),
    Key(
        [],
        "XF86AudioMute",
        lazy.spawn("amixer sset Master 1+ toggle"),
        desc="(Un)Mute Volume"
    ),
    Key(
        [],
        "XF86MonBrightnessDown",
        lazy.spawn("brightnessctl set 5%-"),
        desc="Decrease Brightness"
    ),
    Key(
        [],
        "XF86MonBrightnessUp",
        lazy.spawn("brightnessctl set +5%"),
        desc="Increase Brightness"
    ),
]


groups = [Group(i) for i in "123456789"]

for i in groups:
    keys.extend(
        [
            # mod1 + group number = switch to group
            Key(
                [mod],
                i.name,
                lazy.group[i.name].toscreen(),
                desc="Switch to group {}".format(i.name),
            ),
            # mod1 + shift + group number = move focused window to group
            Key(
                [mod, "shift"],
                i.name,
                lazy.window.togroup(i.name),
                desc="move focused window to group {}".format(i.name)
            ),
        ]
    )

layouts = [
    layout.Columns(
        border_focus=my_theme.colors.magenta,
        border_normal=my_theme.colors.grey,
        border_focus_stack=my_theme.colors.blue,
        border_width=my_theme.border_width,
        margin=my_theme.gap_width,
    ),
]

widget_defaults = dict(
    font="LiberationMono",
    fontsize=13,
    padding=5,
)
extension_defaults = widget_defaults.copy()

def get_random_wallpaper(wallpaper_type: str) -> str:
    wallpaper_dir = "/usr/share/backgrounds/"
    normal_dir = "normal/"
    anime_dir = "anime/"
    if wallpaper_type == "normal":
        wallpaper_dir = wallpaper_dir + normal_dir
    elif wallpaper_type == "anime":
        wallpaper_dir = wallpaper_dir + anime_dir
    else:
        return "invalid wallpaper_type"
    wallpapers = os.listdir(wallpaper_dir)
    num = random.randint(0, len(wallpapers)-1)
    return wallpaper_dir + wallpapers[num]

screens = [
    Screen(
        #wallpaper="/usr/share/backgrounds/normal/fate-city.png",
        wallpaper=get_random_wallpaper("normal"),
        wallpaper_mode="fill",
        top=bar.Bar(
            [
                widget.GroupBox(
                    hide_unused=True,
                    highlight_method="block",
                    this_current_screen_border=my_theme.colors.magenta,
                    this_screen_border=my_theme.colors.magenta,
                    urgent_border=my_theme.colors.red
                ),
                widget.Spacer(),
                widget.Systray(),
                widget.Volume(),
                widget.TextBox("|"),
                widget.Battery(
                    charge_char="CHG",
                    discharge_char="DIS",
                    format="{char}{percent: 2.0%}"
                ),
                widget.TextBox("|"),
                widget.Clock(format="%m/%d/%Y | %I:%M %p"),
            ],
            my_theme.bar_size,
            background=my_theme.colors.black,
            margin=[my_theme.gap_width, my_theme.gap_width, 0, my_theme.gap_width]
        ),
        x11_drag_polling_rate = 60,
    ),
]

# Drag floating layouts.
mouse = [
    Drag(
        [mod],
        "Button1",
        lazy.window.set_position_floating(),
        start=lazy.window.get_position()
    ),
    Drag(
        [mod],
        "Button3",
        lazy.window.set_size_floating(),
        start=lazy.window.get_size()
    ),
    Click(
        [mod],
        "Button2",
        lazy.window.bring_to_front()
    ),
]

dgroups_key_binder = None
dgroups_app_rules = []  # type: list
follow_mouse_focus = True
bring_front_click = False
floats_kept_above = True
cursor_warp = False
floating_layout = layout.Floating(
    border_focus=my_theme.colors.magenta,
    border_normal=my_theme.colors.grey, 
    border_width=my_theme.border_width,
    float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class="confirmreset"),  # gitk
        Match(wm_class="makebranch"),  # gitk
        Match(wm_class="maketag"),  # gitk
        Match(wm_class="ssh-askpass"),  # ssh-askpass
        Match(title="branchdialog"),  # gitk
        Match(title="pinentry"),  # GPG key password entry
        # added by user
        Match(wm_class="Godot"),
        Match(wm_class="mGBA"),
        Match(wm_class="pavucontrol"),
        Match(wm_class="Godot_Engine"),
        Match(wm_class="snes9x-gtk"),
        Match(wm_class="desmume"),
        Match(title="testing"),
    ]
)
auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True

# If things like steam games want to auto-minimize themselves when losing
# focus, should we respect this or not?
auto_minimize = True

# When using the Wayland backend, this can be used to configure input devices.
wl_input_rules = None

wmname = "LG3D"
