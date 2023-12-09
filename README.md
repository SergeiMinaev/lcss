# LCSS
CSS pre-processor written in Python with limited set of features. It's simple and fast.\
The key point is to use as much of native CSS as possible and create as less complexity overhead as possible without compromising productivity.

# Concept
CSS already supports variables, imports and nesting. What CSS really missing is mixins and bundling - these are provided by LCSS.\
LCSS also provides SCSS-like nesting in case if native nesting doesn't meet your needs.

## Variables
Native CSS variables - https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties .
```css
:root {
  --font-mod: 10px;
  --font-size-main: calc(var(--font-mod) + 6px); /* 16px */
}
details {
  font-size: var(--font-size-main);
}
```

## Modules
Native CSS imports - https://developer.mozilla.org/en-US/docs/Web/CSS/@import .\
\
mybtn.lcss:
```css
.mybtn {
  cursor: pointer;
}
```
main.lcss:
```css
@import 'mybtn';

body {
  font-size: 16px;
}
```

## Nesting
CSS supports nesting - https://developer.mozilla.org/en-US/docs/Web/CSS/Nesting_selector .
However it's not 100% equals to SCSS-like nesting we are used to.

Native nesting example:
```css
.parent {
  font-size: 22px;
  a {
    font-size: 16px;
    &:hover {
      font-weight: 900;
    }
  }
}

```
This code is equals to:
```css
.parent {
  font-size: 22px;
}
.parent a {
  font-size: 16px;
}
.parent a:hover {
  font-weight: 900;
}
```
Non-native nesting example:\
\
style.lcss:
```css
.parent {
  &__inner {
    font-size: 22px;
    &:hover {
      font-weight: 900;
    }
  }
}
```
This will be transpiled to:
```css
.parent__inner {
  font-size: 22px;
}
.parent__inner:hover {
  font-weight: 900;
}
```
The main difference is that with native nesting you're not able to use `&` to concatenate selectors as strings.

You can choose preferred nesting method with `NATIVE_NESTING (True/False)` config parameter.

## Mixins
Mixins in LCSS are simple python functions.\
\
mixins.py:
```python
def bg(path):
    return f'''\
    background-image: url({path});
    background-position: center;
    background-repeat: no-repeat;
    background-size: contain;'''
```
style.lcss:
```css
.box {
  .card {
    padding: 10px;
    @mixin bg('bg.webp');
  }
}
```
The result will be the following::
```css
.box .card {
  padding: 10px;
  background-image: url(bg.webp);
  background-position: center;
  background-repeat: no-repeat;
  background-size: contain;
}
```
To make mixins file available, import it in lcss_config.py (see config example below).

## Bundling
LCSS automatically replaces all imports with the content.


# Installation
```bash
pip install lcss
```

# Command line usage
You can use lcss without config file:
```bash
lcss style.lcss > style.css
lcss style.lcss mixins_dir > style.css
```
`mixins_dir` - directory containing `mixins.py` file.\


# Configuration
To use lcss with config file you should create `lcss_config.py` (default one is created automatically by calling `lcss`) in current working directory and then call `lcss` without arguments. 

Example lcss_config.py:
```python
import os
# Mixins in lcss are just a python functions.
# Store mixins in mixins.py file and import it here:
import mixins

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Specify source and output files.
FILES = [
    {
        'in': os.path.join(BASE_DIR, 'style.lcss'),
        'out': os.path.join(BASE_DIR, 'style.css'),
    },
]
# If native nesting is disabled, SCSS-like one will be used instead.
NATIVE_NESTING = False
```

# More examples
You can find some examples in `tests` directory - https://github.com/SergeiMinaev/lcss/tree/dev/tests:
```bash
pip install lcss
git clone git@github.com:SergeiMinaev/lcss.git
cd lcss
lcss tests/nesting_1.lcss
lcss tests/mixins_1.lcss ./tests
```

