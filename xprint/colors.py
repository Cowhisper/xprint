#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Colorize string in terminal
Ref: https://en.wikipedia.org/wiki/ANSI_escape_code
"""

import os
import re
from typing import Union
from .ansi_code import SGR, ESC, RESET, COLORS

# ---------------------------------------------
# Define variables
# ---------------------------------------------

INVALID_COLOR = -1
DEFAULT_COLOR = 0
BIT4_COLOR = 1
RGB_COLOR = 2


COLOR_MAP = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'magenta': (255, 0, 255),
    'cyan': (0, 255, 255),
    'white': (255, 255, 255),
}

# ---------------------------------------------
# color functions
# ---------------------------------------------

def is_256color_terminal():
    """
    Check if the current terminal supports 256 colors.

    Returns:
        bool: True if the terminal supports 256 colors, False otherwise.

    Example:
        is_supported = is_256color_terminal()
        print(is_supported)  # True or False
    """
    term = os.environ.get('TERM', '')
    if term in ('xterm', 'xterm-256color', 'screen', 'screen-256color'):
        return True
    else:
        return False


def register_color(name, color):
    """
    register color
    """
    COLOR_MAP[name] = color


def len_cstring(string):
    """
    get length of a colored string
    """
    pat = re.compile('\\033\[([0-9|;]*)m(.*)\\033\[0m')
    info = pat.findall(string)
    if len(info) == 0:
        return len(string)
    else:
        return len(''.join([i[1] for i in info]))


def _parse_color(color):
    if isinstance(color, list) or isinstance(color, tuple):
        if len(color) == 3 and max(color) < 256 and min(color) >= 0:
            color = list(map(int, color))
            return f'{color[0]};{color[1]};{color[2]};'
        return ''
    elif isinstance(color, str):
        if len(color) == 0 or color == 'default':
            return ''
        elif color[0] == '#':
            try:
                hexcode = color.lstrip('#')
                hlen = len(hexcode)
                rgb = list(int(hexcode[i:i + hlen // 3], 16)
                           for i in range(0, hlen, hlen // 3))
                return _parse_color(rgb)
            except:
                return ''
        else:
            color = COLORS.get_code(color.lower())
            return color
    return ''


def _parse_color_type(color):
    if isinstance(color, list) or isinstance(color, tuple):
        if len(color) == 3 and max(color) < 256 and min(color) >= 0:
            return RGB_COLOR
        return INVALID_COLOR
    elif isinstance(color, str):
        if len(color) == 0 or color == 'default':
            return DEFAULT_COLOR
        elif color[0] == '#':
            try:
                hexcode = color.lstrip('#')
                hlen = len(hexcode)
                rgb = list(
                    int(hexcode[i:i + hlen // 3], 16)
                    for i in range(0, hlen, hlen // 3)
                )
                return RGB_COLOR
            except Exception:
                return INVALID_COLOR
        else:
            color = COLORS.get_code(color.lower())
            return BIT4_COLOR
    return INVALID_COLOR


def _parse_option(kwargs, option):
    if len(option) == 0:
        return kwargs
    for op in option.split('|'):
        try:
            kw, param = op.split(':')
            if param[0] == '(' and param[-1] == ')':
                param = eval(param)
            kwargs[kw] = param
        except Exception:
            pass
    return kwargs


def _parse_complex_mode(string):
    pat = re.compile('\$\[([a-z|\||:|\(|0-9|,|\)]*)\]\((.*?)\)')
    # pat = re.compile('\$\[([a-z|\||:|\(|\)]*)\]\((.*?)\)')
    segm = pat.split(string)
    opts = {x[0]: x[1] for x in pat.findall(string)}
    ret = ''
    option = ''
    for idx, s in enumerate(segm):
        if s in opts:
            option = s
            continue
        else:
            if option != '':
                ret += colorize(s, option=option)
                option = ''
            else:
                ret += s
    return ret


def bit4_colorize(
        string: str,
        fg: str = '',
        bg: str = '',
        sgr: str = '',
        bright: bool = False,
        **kwargs):
    """
    Colorize a string using 8-bit colors in a terminal.

    Args:
        string (str): The input string to be colorized.
        fg (str): 
            The foreground color. It can be specified as a full name or abbreviation of colors: BLACK, RED, GREEN, YELLOW, BLUE, CYAN, MAGENTA, WHITE, or DEFAULT.
        bg (str): 
            The background color. Same format as `fg`.
        sgr (str): 
            The style of the input string. It can be specified as a full name or abbreviation of styles: NORMAL, BOLD, FAINT, ITALIC, UNDERLINE.
        bright (bool): 
            Whether to use bright colors or not.

    Returns:
        str: The input string with the specified foreground color, background color, and style applied.
    """

    fg_color = _parse_color(fg)
    bg_color = _parse_color(bg)
    sgr_code = SGR.get_code(sgr.lower())
    if sgr_code:
        sgr_code += ';'

    if bright:
        fg_code = ('9' + fg_color + ';') if fg_color else ''
        bg_code = ('10' + bg_color + ';') if bg_color else ''
    else:
        fg_code = ('3' + fg_color + ';') if fg_color else ''
        bg_code = ('4' + bg_color + ';') if bg_color else ''

    code = f'{sgr_code}{fg_code}{bg_code}'
    if len(code) > 0 and code[-1] == ';':
        code = code[:-1]

    return f'{ESC}[{code}m{string}{RESET}'


def rgb_colorize(
        string: str,
        fg: Union[tuple, list, str] = (),
        bg: Union[tuple, list, str] = (),
        sgr: str = '',
        **kwargs):
    """
    Colorize a string using RGB colors.

    Args:
        string (str): The input string to be colorized.
        fg (Union[tuple, list, str], optional): 
            The foreground color. It can be specified as an RGB tuple, RGB list, or HEX RGB color. Defaults to an empty tuple ().
        bg (Union[tuple, list, str], optional): 
            The background color. Same format as `fg`. Defaults to an empty tuple ().
        sgr (str, optional): 
            The style of the input string. It can be specified as a full name or abbreviation of the following styles: 
            "NORMAL", "BOLD", "FAINT", "ITALIC", "UNDERLINE". Defaults to an empty string.

    Returns:
        str: The input string with the specified foreground color, background color, and style applied.
    """

    fg_code = _parse_color(fg)
    bg_code = _parse_color(bg)
    if fg_code:
        fg_code = '38;2;' + fg_code
    if bg_code:
        bg_code = '48;2;' + bg_code

    sgr_code = SGR.get_code(sgr.lower())
    if sgr_code:
        sgr_code += ';'

    code = f'{sgr_code}{fg_code}{bg_code}'
    if len(code) > 0 and code[-1] == ';':
        code = code[:-1]

    return f'{ESC}[{code}m{string}{RESET}'


def colorize(
        string: str,
        fg: Union[tuple, list, str] = 'default',
        bg: Union[tuple, list, str] = 'default',
        sgr: str = '',
        option: str = None,
        use_parser: bool = False,
        **kwargs):
    """
    Colorize a string using RGB colors or 8-bit color.

    Args:
        string (str): The input string to be colorized.
        fg (Union[tuple, list, str], optional): 
            The foreground color. It can be specified as an RGB tuple, RGB list, 
            HEX RGB color or a string representing an 8-bit color or "default". Defaults to 'default'.
        bg (Union[tuple, list, str], optional): 
            The background color. Same format as `fg`. Defaults to 'default'.
        sgr (str, optional): 
            The style of the input string. It can be specified as a full name or abbreviation of the following styles: 
            "NORMAL", "BOLD", "FAINT", "ITALIC", "UNDERLINE". Defaults to ''.
        option (str, optional): 
            The colorize option. It follows the format: 
            `option = f"fg:{fg}|bg:{bg}|sgr:{sgr}"`. This allows for more complex colorization options. Defaults to None.
        use_parser (bool, optional): 
            If True, the function will parse the input string for colorize options enclosed in `$[]()`. Defaults to False.
        **kwargs: Additional keyword arguments that can be used to customize the colorization.

    Returns:
        str: The colored string.

    Raises:
        OSError: If the terminal does not support 256 colors and 8-bit color is used.

    Example Usage:
        # Example 1: Applying RGB color and style to a string
        colored_string = colorize("Hello World", fg=(255, 0, 0), bg=(0, 0, 255), sgr="bold")
        print(colored_string)  # Prints the string in red foreground, blue background, and bold style

        # Example 2: Applying 8-bit color and style to a string
        colored_string = colorize("Hello World", fg="red", bg="blue", sgr="bold", bright=True)
        print(colored_string)  # Prints the string in bright red foreground, bright blue background, and bold style

        # Example 3: Applying colorize option to a string
        colored_string = colorize("Hello World", option="fg:(0,255,0)|sgr:italic")
        print(colored_string)  # Prints the string in green foreground and italic style
    """

    if use_parser:
        return _parse_complex_mode(string)

    def get_color(c):
        ctype = _parse_color_type(c)
        if ctype in (DEFAULT_COLOR, INVALID_COLOR):
            return "default", ctype
        elif ctype == BIT4_COLOR:
            if not is_256color_terminal():
                raise OSError("Terminal does not support 256 colors, please use bit4_colorize instead.")
            else:
                return COLOR_MAP.get(c, 'default'), ctype
        return c, ctype

    kwargs.update({
        'string': string,
        'fg': fg,
        'bg': bg,
        'sgr': sgr,
        'option': None,
    })
    if option:
        kwargs = _parse_option(kwargs, option)

    kwargs['fg'], fg_ctype = get_color(kwargs['fg'])
    kwargs['bg'], bg_ctype = get_color(kwargs['bg'])

    return rgb_colorize(**kwargs)


def cprint(
        string: str,
        fg: Union[tuple, list, str] = 'default',
        bg: Union[tuple, list, str] = 'default',
        sgr: str = '',
        option: str = None,
        use_parser: bool = False,
        **kwargs):
    """
    colorize print function. Parmas same as `colorize`.
    """
    print(colorize(string, fg, bg, sgr, option, use_parser, **kwargs))
