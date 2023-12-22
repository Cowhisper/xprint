#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
sys.path.append('.')
from xprint.colors import bit8_colorize, rgb_colorize, colorize, cprint


# test bit4
print('test 4 bit color')
cprint('xprint', fg='blue', sgr='bold')
cprint('xprint', fg='blue', sgr='normal')
cprint('xprint', fg='blue', sgr='normal', bright=True)
cprint('xprint', fg='blue', sgr='faint')
cprint('xprint', fg='blue', sgr='italic')
cprint('xprint', fg='blue', sgr='underline')
cprint('xprint', fg='blue', bg='red')

# test rgb
print('test rgb color')
cprint('xprint', fg=(255, 255, 0), sgr='bold')
cprint('xprint', fg=(255, 255, 0), sgr='normal')
cprint('xprint', fg=(255, 255, 0), sgr='normal', bright=True)
cprint('xprint', fg=(255, 255, 0), sgr='faint')
cprint('xprint', fg=(255, 255, 0), sgr='italic')
cprint('xprint', fg=(255, 255, 0), sgr='underline')
cprint('xprint', fg=(255, 255, 0), bg=(0, 0, 255))

# test option
print('test option')
cprint('xprint', option='fg:(255,0,0)|bg:(0,0,255)|sgr:bold')
cprint('xprint', option='fg:(255,0,0)|bg:(0,0,255)|sgr:normal')
cprint('xprint', option='fg:(255,0,0)|bg:(0,0,255)|sgr:faint')
cprint('xprint', option='fg:(255,0,0)|bg:(0,0,255)|sgr:italic')
cprint('xprint', option='fg:(255,0,0)|bg:(0,0,255)|sgr:underline')
