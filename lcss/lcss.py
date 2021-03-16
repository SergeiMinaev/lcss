#!/bin/env python
import os, re, sys


EXAMPLE_CONF = """import os
# Mixin in lcss is just a python function. Comment it if you doesn't have mixins.
from frontend.src.css import mixins

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

FILES = [
    {
        'in': os.path.join(BASE_DIR, 'frontend/src/css/style.lcss'),
        'out': os.path.join(BASE_DIR, 'static/css/style.css'),
    },
    #{
    #    'in': os.path.join(BASE_DIR, 'frontend/src/css/style-dark.lcss'),
    #    'out': os.path.join(BASE_DIR, 'static/css/style-dark.css'),
    #},
]
"""
sys.path.insert(0, os.getcwd())
if not os.path.isfile('conf_lcss.py'):
    print('Config conf_lcss.py not found.')
    f = open('conf_lcss.py', 'w')
    f.write(EXAMPLE_CONF)
    f.close()
    print('Default config was created in current dir. Edit it and re-start me.')
    sys.exit(0)
else:
    import conf_lcss as conf


cur = None
cl_list= []

def process(data, src_dir):
    r = ''
    cur = ''
    for line in data.split('\n'):
        line = line.strip()
        if line.startswith(('.', '#')):
            cur = line.split(' ')[0]
            cl_list.append(cur)
            r += cur + ' {\n'
        elif line.startswith('&'):
            part = line[1:-1].strip()
            if part.startswith(('_', '-')):
                cur = cur + part
            else:
                cur = cur + ' ' + part
            cl_list.append(cur)
            r += '} ' + cur + ' {\n'
        elif line.startswith('}'):
            if len(cl_list) > 0:
                cl_list.pop()
            cur = cl_list[-1:][0] if len(cl_list) > 0 else None
            if not cur:
                r += line
        elif line.startswith('@import'):
            fname = line.split('@import')[1]
            fname = re.sub('\"|\'|;| ', '', fname)
            f = open(os.path.join(conf.BASE_DIR, src_dir, fname), 'r')
            r += process(f.read(), src_dir)
        elif line.startswith('@'):
            name, args_s = re.match("^@(.+)\((.+)\)", line).groups()
            args = []
            for arg in args_s.split(','):
                arg = arg.strip().replace('"', '').replace("'", '')
                args.append(arg)
            if (f := getattr(mixins, name, None)):
                r += f(*args)
        else:
            r += line + '\n'
    return r+'\n'


for files in conf.FILES:
    src_dir = os.path.dirname(files['in'])
    f = open(files['in'], 'r')
    data = f.read()
    f.close()


    f = open(files['out'], 'w')
    out = process(data, src_dir)
    f.write(out)
    f.close()
    #print(out)

