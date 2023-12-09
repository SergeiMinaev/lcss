import re
import difflib
import lcss
from lcss.main import transpile, minify, add_linebreaks
from tests import mixins


SRC_DIR = './tests'


def prepare_to_diff(s):
    return add_linebreaks(minify(s))

def check(name, native_nesting=False):
    src = open(f'tests/{name}.lcss').read()
    result = prepare_to_diff(transpile(src, SRC_DIR, mixins, native_nesting))
    correct = prepare_to_diff(open(f'tests/{name}.css').read())
    try:
        assert result == correct
    finally:
        #print('Result:\n')
        #print(result)
        #print('Correct:\n')
        #print(correct)
        print('Short diff:\n')
        for text in difflib.unified_diff(correct.split("\n"), result.split("\n")):
            if text[:3] not in ('+++', '---', '@@ '):
                print(text)


def test_vanilla_1(): check('vanilla_1')


def test_nesting_1(): check('nesting_1')


def test_nesting_2(): check('nesting_2')


def test_imports_1(): check('imports_1')


def test_mixins_1(): check('mixins_1')


def test_fontface_1(): check('fontface_1')


def test_native_nesting_1(): check('native_nesting_1', native_nesting=True)
