import re
import lcss
from tests import mixins


SRC_DIR = './tests'


def normalize(s):
    r = re.sub(' +', ' ', s)
    r = re.sub('\n', '', r)
    r = re.sub(r'\s*([{}:;])\s*', r'\1', r)
    return add_linebreaks(r)


def add_linebreaks(s):
    return re.sub(r'([{};])', r'\1\n', s)


def check(name):
    src = open(f'tests/{name}.lcss')
    src = normalize(src.read())
    out = normalize(lcss.transpile(src, SRC_DIR, mixins))
    correct_out = open(f'tests/{name}.css')
    correct_out = normalize(correct_out.read())
    assert out == correct_out


def test_vanilla_1(): check('vanilla_1')


def test_nesting_1(): check('nesting_1')


def test_nesting_2(): check('nesting_2')


def test_imports_1(): check('imports_1')


def test_mixins_1(): check('mixins_1')
