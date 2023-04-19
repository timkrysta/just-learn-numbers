"""
Color	                        Foreground	Background
Black	                        \033[30m	\033[40m
Red	                            \033[31m	\033[41m
Green	                        \033[32m	\033[42m
Orange	                        \033[33m	\033[43m
Blue	                        \033[34m	\033[44m
Magenta	                        \033[35m	\033[45m
Cyan	                        \033[36m	\033[46m
Light gray	                    \033[37m	\033[47m
Fallback to distro's default	\033[39m	\033[49m
"""

class Color:
    CYAN      = '\033[96m'
    GREEN     = '\033[92m'
    DARKGREEN = '\033[32m'
    DARKRED   = '\033[31m'
    PURPLE    = '\033[95m'
    DEFAULT   = '\033[39m'

    BOLD      = '\033[1m'
    UNDERLINE = '\033[4m'
    END       = '\033[0m' # No Color

nbsp_x1 = " "
nbsp_x3 = "   " # non breaking space 3 times
nbsp_x4 = "    "
padding = nbsp_x1

class Icon(Color):
    tick     = Color.BOLD + Color.GREEN     + u"\u2713"  + Color.END + padding
    cross    = Color.BOLD + Color.DARKRED   + u"\u00d7 " + Color.END + padding
    info     = Color.BOLD + Color.CYAN      + "i"        + Color.END + padding
    question =              Color.DARKGREEN + "?"        + Color.END + padding

def style_string(style, string):
    return f"{style}{string}{Color.END}"