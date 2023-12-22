#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
from .ansi_code import *


def flush(lines: int = 1):
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
