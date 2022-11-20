#!/bin/env python
import os
import re
import sys


EXAMPLE_CONF = """import os
# Mixins in lcss are just a python functions.
# Store mixins in mixins.py file and import it like this:
# from foo.bar import mixins

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Use FILES to specify source and output files.
FILES = [
    #{
    #    'in': os.path.join(BASE_DIR, 'frontend/src/style/style.lcss'),
    #    'out': os.path.join(BASE_DIR, 'static/style/style.css'),
    #},
]
"""


def check_config():
    sys.path.insert(0, os.getcwd())
    if not os.path.isfile('lcss_config.py'):
        print('Config lcss_config.py not found. Creating a new one.')
        f = open('lcss_config.py', 'w')
        f.write(EXAMPLE_CONF)
        f.close()
        print('Default config lcss_config.py was created in current dir.'
              + ' Edit it to suit your needs and try again.')


def normalize(s):
    s = re.sub(' +', ' ', s)
    s = re.sub('\n', '', s)
    s = re.sub(r'\s*([{}:;])\s*', r'\1', s)
    return s


def add_linebreaks(s): return re.sub(r'([{};])', r'\1\n', s)


def transpile(data, src_dir, mixins=None):
    """
    Main function to convert LCSS string to CSS.
    """
    data = load_imports(data, src_dir)
    r = handle_mixins(flatify(nested_dict(data)), mixins)
    return r


def nested_dict(data):
    """
    Convert LCSS string to a dict.
    """
    level = 0
    parents = []
    rules = {}
    for line in data.split('\n'):
        line = line.strip()
        if '{' in line:
            level += 1
            selector = line.replace('{', '')
            parents.append(selector)
        elif '}' in line:
            level -= 1
            if len(parents) > 0:
                parents.pop()
        elif not line:
            continue
        obj = rules
        for key in parents:
            if key not in obj:
                obj[key] = {}
            obj = obj[key]
        if '{' not in line and '}' not in line:
            if '_values' not in obj:
                obj['_values'] = []
            obj['_values'].append(line)
    return rules


def flatify(obj, path=[], r=''):
    """
    Convert dict created by nested_dict() to LCSS string.
    All nested rules will be flattened.
    """
    level = 0
    if type(obj) is dict:
        for k in obj.keys():
            if k.startswith('@') and not k.startswith('@mixin'):
                r += k + ' {\n'
                level += 1
                r = flatify(obj[k], path, r)
            elif k.startswith('@supports'):
                r += k + ' {\n'
            elif k == '_values':
                r += get_selector(path) + ' {\n'
                r += '    ' + stringify_values(obj[k]) + '\n'
                r += '}\n'
            else:
                path.append(k)
                r = flatify(obj[k], path, r)
            while level > 0:
                r += '}\n'
                level -= 1
        if len(path) > 0:
            path.pop()
    return r


def stringify_values(vals):
    """
    ['color:red;', 'padding:0;'] -> 'color:red;\npadding:0;'
    """
    return '\n'.join(vals)


def get_selector(parents):
    """
    ['.box', '&__inner', '& img'] -> '.box__inner img'
    """
    if parents and parents[0].startswith('@keyframes'):
        return str(parents)
    r = ''
    for p in parents:
        r += p.strip()
    return r.replace('&', '')


def handle_mixins(data, mixins=None):
    for line in data.split('\n'):
        line = line.strip()
        if line.startswith('@mixin '):
            name, args_s = re.match(r"^@mixin (.+)\((.+)?\)", line).groups()
            args = []
            if args_s:
                for arg in args_s.split(','):
                    arg = arg.strip().replace('"', '').replace("'", '')
                    args.append(arg)
            if not mixins:
                raise Exception(f'A mixin "{name}" was found but `mixins` module is not loaded')
            if (f := getattr(mixins, name, None)):
                mixin_res = f(*args)
                data = data.replace(line, mixin_res)
            else:
                raise Exception(f'Mixin not found: {name}')
    return data


def load_imports(data, src_dir):
    data = add_linebreaks(normalize(data))
    r = ''
    for line in data.split('\n'):
        if line.startswith('@import'):
            fname = line.split('@import')[1]
            fname = re.sub(r'\"|\'|;| ', '', fname)
            f = open(os.path.join(src_dir, fname + '.lcss'), 'r')
            r += load_imports(f.read(), src_dir)
    data = re.sub(r'@import.+?;', '', data)
    return r + data


def run():
    if (path := sys.argv[1] if len(sys.argv) > 1 else None):
        if len(sys.argv) == 3:
            sys.path.append(sys.argv[2])
            import mixins
        else:
            mixins = None
        src = open(path)
        src_dir = os.path.dirname(path)
        out = transpile(src.read(), src_dir, mixins)
        print(out)
    else:
        check_config()
        import lcss_config as conf
        mixins = getattr(conf, 'mixins', None)

        if len(conf.FILES) == 0:
            print('No source files specified in lcss_config.py. Exiting.')
            return
        for files in conf.FILES:
            src_dir = os.path.dirname(files['in'])
            f = open(files['in'], 'r')
            data = f.read()
            f.close()

            f = open(files['out'], 'w')
            out = transpile(data, src_dir, mixins)
            f.write(out)
            f.close()
            print(os.path.basename(files['in']), '->', os.path.basename(files['out']))
        print('Done')
