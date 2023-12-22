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


INVALID_COLOR = -1
DEFAULT_COLOR = 0
BIT4_COLOR = 1
RGB_COLOR = 2


BIT4_COLOR_MAP = {
    'black': (0, 0, 0),
    'red': (255, 0, 0),
    'green': (0, 255, 0),
    'yellow': (255, 255, 0),
    'blue': (0, 0, 255),
    'magenta': (255, 0, 255),
    'cyan': (0, 255, 255),
    'white': (255, 255, 255),
}


def is_256color_terminal():
    term = os.environ.get('TERM', '')
    if term in ('xterm', 'xterm-256color', 'screen', 'screen-256color'):
        return True
    else:
        return False


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
    colorize a string using 4 bit colors.

    Params:
        string: input string
        fg:     foreground color. support both full-name & abbrev of
                colors: BLACK, RED, GREEN, YELLOW, BLUE, CYAN,
                MAGENTA, WHITE or DEFAULT
        bg:     background color. same as fg.
        sgr:    style of input string. support both full-name / abbrev of
                sgrs: NORMAL, BOLD, FAINT, ITALIC, UNDERLINE
        bright: bright color or not.

    Return:
        colored string
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
    colorize a string using rgb colors.

    Params:
        string: input string
        fg:     foreground color. support both rgb list / tuple & hex color
                Eg. #FFFADA or (255, 0, 0)
        bg:     background color. same as fg.
        sgr:    style of input string. support both full-name / abbrev of
                sgrs: NORMAL, BOLD, FAINT, ITALIC, UNDERLINE

    Return:
        colored string
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
    colorize a string using rgb colors or 4 bit color.

    Params:
        string: input string
        fg:     foreground color. support both rgb format & 4 bit color.
                see details at function `bit4_colorize` and `rgb_colorize`
        bg:     background color. same as fg.
        sgr:    style of input string. support both full-name / abbrev of
                sgrs: NORMAL, BOLD, FAINT, ITALIC, UNDERLINE
        option: colorize option. The option follow the rule:
                option = f"fg:{fg}|bg:{bg}|sgr:{sgr}"
                Eg.
                >>> ctring = colorize('xprint', option='fg:(0,255,0)|sgr:italic')

    Return:
        colored string
    """

    if use_parser:
        return _parse_complex_mode(string)

    def get_color(c):
        ctype = _parse_color_type(c)
        if ctype in (DEFAULT_COLOR, INVALID_COLOR):
            return "default"
        elif ctype == BIT4_COLOR:
            if not is_256color_terminal():
                raise OSError('terminal do not support 256 color, use bit4_colorize instead')
            else:
                return BIT4_COLOR_MAP.get(c, 'default')
        return c

    kwargs.update({
        'string': string,
        'fg': fg,
        'bg': bg,
        'sgr': sgr,
        'option': None,
    })
    if option:
        kwargs = _parse_option(kwargs, option)

    kwargs['fg'] = get_color(kwargs['fg'])
    kwargs['bg'] = get_color(kwargs['bg'])

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
