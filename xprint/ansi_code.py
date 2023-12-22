#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import namedtuple


ANSICODE = namedtuple("ANSICODE", ['name', 'abbrev', 'code'])

ESC = '\033'
RESET = ESC + '[0m'
DEFAULT = ANSICODE('DEFAULT', ['default'], '')


class ANSICODES(object):
    def __init__(self, ansicodes):
        self._names = {}
        self._abbrevs = {}
        self._codes = {}
        
        for ac in ansicodes + [DEFAULT]:
            setattr(self, ac.name, ac)
            self._names[ac.name] = ac
            self._abbrevs[ac.name.lower()] = ac
            for ab in ac.abbrev:
                self._abbrevs[ab] = ac
            self._codes[ac.code] = ac

    def get(self, inp, field=None):
        if inp in self._names:
            ac = self._names[inp]
        elif inp in self._abbrevs:
            ac = self._abbrevs[inp]
        elif inp in self._codes:
            ac = self._codes[inp]
        else:
            ac = DEFAULT

        if field is None:
            return ac
        else:
            return getattr(ac, field)

    def get_code(self, inp):
        return self.get(inp, 'code')


# SGR (Select Graphic Rendition) parameters

# reset / normal
NORMAL     = ANSICODE('NORMAL',     ['normal'],     '0')
BOLD       = ANSICODE('BOLD',       ['bold'],       '1')
FAINT      = ANSICODE('FAINT',      ['faint'],      '2')
ITALIC     = ANSICODE('ITALIC',     ['italic'],     '3')
UNDERLINE  = ANSICODE('UNDERLINE',  ['underline'],  '4')

SGR = ANSICODES([NORMAL, BOLD, FAINT, ITALIC, UNDERLINE])

# 4 bit color
BLACK   = ANSICODE('BLACK',  ['black'], '0')
RED     = ANSICODE('RED',    ['red', 'r'], '1')
GREEN   = ANSICODE('GREEN',  ['green', 'g'], '2')
YELLOW  = ANSICODE('YELLOW', ['yellow', 'y'], '3')
BLUE    = ANSICODE('BLUE',   ['blue'], '4')
MAGENTA = ANSICODE('MAGENTA', ['magenta', 'm'], '5')
CYAN    = ANSICODE('CYAN',   ['cyan', 'c'], '6')
WHITE   = ANSICODE('WHITE',  ['white', 'w'], '7')

COLORS = ANSICODES([BLACK, RED, GREEN, YELLOW, BLUE, CYAN, MAGENTA, WHITE])
