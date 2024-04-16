# X-print

X-print is a package used to enrich functionality of `print`. 

# HightLights
- **color print**: support foreground & background color customization.
- **SGR (Select Graphic Rendition)**: support common SGR: BOLD / FAINT / ITALIC / UNDERLINE
- **multiple lines print flushing**

# Install
```bash
$ git clone <this repo>
$ cd <this repo>
$ pip install .
```

# Usage

## color print
```python
from xprint.colors import cprint, register_color

# 4 bit color print
cprint('xprint', fg='blue', bg='yellow', sgr='bold')

# 16 bit rgb color print, support both rgb color tuple and hex color string
cprint('xprint', fg=(0, 0, 255), bg='#808000', sgr='italic')

# pass option to colorize
cprint('xprint', option='fg:(255,0,0)|bg:(0,0,255)|sgr:bold')

# color render template: render a string by format '$[option](text)'
cprint('$[bg:cyan|fg:(0,255,0)|sgr:bold](xprint) is great and $[bg:red|fg:(0,255,0)|sgr:italic](handy) ', use_parser=True)

# register color
register_color('olive', '#808000')
cprint('$[bg:cyan|fg:olive|sgr:bold](xprint)', use_parser=True)
```

## flushing
Typically we could use `sys.stdout.flush()` to flush one line of text ending with `'\r'`. But multiple lines flushing is kind of tricky.
We offer a handy way to perform multiple lines flushing.
```python
from xprint.flush import flush, Flushing
import time

# option 1
for i in range(100000):
    x = f'{i%10}'
    y = f'{i%100}'
    z = f'{i%1000}'

    print(x)
    print(y)
    print(z, end='')
    flush(3)
    time.sleep(0.1)

# option 2
for i in range(100000):
    with Flushing(3) as f:
        f.print(f'{i%10}')
        f.print(f'{i%100}')
        f.print(f'{i%1000}')
    time.sleep(0.1)
```

## tablize
a easy way to print strings in a table-like format.
```python
from xprint.tablize import tablize

slist = ['apple', 'banana', 'cherry', 'elderberry', 'grape']
cols = 2
col_ws = [10, 5]
sep = '|'
pad = True
line_prefix = ['|', '|', '|']
line_suffix = ['|', '|', '|']
table = tablize(slist, cols, col_ws, sep, pad, line_prefix, line_suffix)
# Output
# |apple     |banan|
# |cherry    |elder|
# |grape     |     |
```


# Reference
All the functionality are implemented base on `https://en.wikipedia.org/wiki/ANSI_escape_code`
