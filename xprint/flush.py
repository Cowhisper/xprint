#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from .ansi_code import *


def flush(lines: int = 1):
    """
    Flush content in terminal. Default flush 1 line.
    Args:
        lines: number of lines to flush
    
    Usage:
        >>> for i in range(iteration):
        >>>     print(line1)
        >>>     print(line2)
        >>>     print(line3, end='')
        >>>     flush(3)
    """
    if lines <= 0:
        return
    elif lines == 1:
        sys.stdout.flush()
    else:
        sys.stdout.write(ESC + '[{}A\r'.format(lines - 1))


class Flushing:
    """
    Flushing content in terminal.

    Param:
        lines: number of lines to flush

    Usage:
        >>> for i in range(iteration):
        >>>     with Flushing(3) as f:
        >>>         f.print(line1)
        >>>         f.print(line2)
        >>>         f.print(line3)
    """
    def __init__(self, lines):
        self.lines = lines
        self.cnt = 0

    def print(self, string):
        if self.cnt < self.lines-1:
            print(string)
        elif self.cnt == self.lines-1:
            print(string, end='')
        else:
            raise IndexError(
                f'string (line index: {self.cnt}) to be printed is out of range of Flushing ({self.lines}).')
        self.cnt += 1

    def flush(self):
        flush(self.cnt)

    def __enter__(self):
        self.cnt = 0
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.flush()


def flush_print(s: str):
    """
    print a string with flush. Input string contains lines which are seperated by '\r'.

    Eg.
        >>> for i in range(iteration):
        >>>     flush_print(f'{i}\r{i+1}\r{i+2}')
        >>>     time.sleep(0.5)
    """
    lines = s.split('\r')
    for line in lines[:-1]:
        print(line)
    print(lines[-1], end='')
    flush(len(lines))