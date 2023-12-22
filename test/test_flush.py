#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
sys.path.append('.')
from xprint.flush import flush, Flushing
import time


def test_flush():
    for i in range(100000):
        x = f'{i%10}'
        y = f'{i%100}'
        z = f'{i%1000}'

        print(x)
        print(y)
        print(z, end='')
        flush(3)
        time.sleep(0.1)


def test_flushing():
    for i in range(100000):
        with Flushing(3) as f:
            f.print(f'{i%10}')
            f.print(f'{i%100}')
            f.print(f'{i%1000}')
            # f.print(f'{i%10}')
        time.sleep(0.1)


test_flush()
# test_flushing()
