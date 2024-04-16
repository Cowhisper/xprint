#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
import random
import time
from xprint.colors import colorize, is_256color_terminal
from xprint.flush import Flushing


PATTERN = """
                              _|              _|      
_|    _|  _|_|_|    _|  _|_|      _|_|_|    _|_|_|_|  
  _|_|    _|    _|  _|_|      _|  _|    _|    _|      
_|    _|  _|    _|  _|        _|  _|    _|    _|      
_|    _|  _|_|_|    _|        _|  _|    _|      _|_|  
          _|                                          
          _|                                          
"""
# generate by https://zh.rakko.tools/tools/68/ @blocks2

def generate_random_color():
    cs = list(range(256))
    r = random.choice(cs)
    g = random.choice(cs)
    b = random.choice(cs)
    return f'({r},{g},{b})'

class Pattern(object):
    def __init__(self, pstr: str) -> None:
        self.pstr = pstr
        self.lines = pstr.split('\n')[1:]
        self.height = len(self.lines)
        self.width = max([len(line) for line in self.lines]) // 2
        self.reset()
    def reset(self):
        self.show = [' ' * (self.width * 2)] * self.height
        self.step_idx = -1
    def step(self):
        self.step_idx += 1
        if self.step_idx >= self.width:
            st_idx = 2 * (self.width - self.step_idx % self.width - 1)
            for i in range(self.height):
                self.show[i] = self.lines[i][st_idx:] + self.lines[i][:st_idx]
            return self.show
        st_idx = 2 * (self.width - self.step_idx - 1)
        for i in range(self.height):
            self.show[i] = self.lines[i][st_idx:]
        return self.show

def print_xprint_ascii(pattern):
    print('is_256color_terminal:', is_256color_terminal())
    pat = Pattern(pattern)
    while True:
        color = generate_random_color()
        for i in range(pat.width):
            lines = pat.step()
            with Flushing(pat.height) as f:
                for line in lines:
                    f.print(colorize(line, fg=eval(color)))
            time.sleep(0.15)
            


if __name__ == '__main__':
    print_xprint_ascii(PATTERN)
