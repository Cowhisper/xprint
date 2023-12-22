#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
import random
import time
from xprint.colors import *
from xprint.tablize import tablize
from xprint.flush import Flushing


def generate_random_color():
    cs = list(range(256))
    r = random.choice(cs)
    g = random.choice(cs)
    b = random.choice(cs)
    return f'({r},{g},{b})'


def generate_random_color_string(string):
    fg = generate_random_color()
    bg = generate_random_color()
    cstring = colorize(string, option=f'fg:{fg}|bg:{bg}')
    return cstring


def test_tablize():
    for i in range(100):
        with Flushing(5) as f:
            slist = [
                generate_random_color_string('xprint') for i in range(50)]
            rlist = tablize(
                slist, cols=10, col_ws=[-1]*10, sep='|',
                pad=True, line_prefix='|', line_suffix='|')
            rlist = rlist.strip().split('\n')
            for line in rlist:
                f.print(line)
        time.sleep(0.2)


test_tablize()
