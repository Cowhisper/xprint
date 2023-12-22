#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math
from .colors import len_cstring


def _tablize(slist, cols, col_ws=[], sep='\t', pad=True, line_prefix=[], line_suffix=[]):
    assert cols > 0, 'cols should be positive integer.'
    if isinstance(col_ws, int):
        col_ws = [col_ws for i in range(cols)]
    rows = math.ceil(len(slist) / cols)
    if isinstance(line_prefix, str):
        line_prefix = [line_prefix for i in range(rows)]
    if isinstance(line_suffix, str):
        line_suffix = [line_suffix for i in range(rows)]
    if isinstance(line_prefix, list):
        if len(line_prefix) == 0:
            line_prefix = ['' for i in range(rows)]
        elif len(line_prefix) < rows:
            line_prefix += [''] * (len(line_prefix) - rows)

    if isinstance(line_suffix, list):
        if len(line_suffix) == 0:
            line_suffix = ['' for i in range(rows)]
        elif len(line_suffix) < rows:
            line_suffix +=  [''] * (len(line_suffix) - rows)

    if pad:
        slist += [''] * (rows * cols - len(slist))

    cols_dic = {i: [] for i in range(cols)}
    for idx, s in enumerate(slist):
        cols_dic[idx % cols].append(s)
    if len(col_ws) == 0:
        col_ws = [max([len(_) for _ in cols_dic[i]]) for i in range(cols)]

    rlist = [''] * len(slist)
    for idx, s in enumerate(slist):
        row = idx // cols
        if (idx+1) % cols == 0:
            suffix = line_suffix[row] + '\n'
        else:
            suffix = sep

        if idx % cols == 0:
            prefix = line_prefix[row]
        else:
            prefix = ''
        ws = col_ws[idx % cols]
        if ws > 0:
            rlist[idx] = prefix + '{{:<{}s}}'.format(ws).format(slist[idx])[:ws] + suffix
        else:
            rlist[idx] = prefix + '{}'.format(slist[idx]) + suffix
 
    return rlist


def tablize(slist, cols, col_ws=[], sep='\t', pad=True, line_prefix=[], line_suffix=[]):
    return ''.join(_tablize(slist, cols, col_ws, sep, pad, line_prefix, line_suffix))


def tprint(slist, cols, col_ws=[], sep='\t', flush=False, pad=True, line_prefix=[], line_suffix=[]):
    print(tablize(slist, cols, col_ws, sep, pad, line_prefix, line_suffix))

        
