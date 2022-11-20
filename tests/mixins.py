def flex():
    return '''\
display: flex;
justify-content: center;
align-items: center;'''


def bg(path):
    return f'''\
background-image: url({path});
background-position: center;
background-repeat: no-repeat;
background-size: contain;'''


def user_select(prop):
    return f'''\
  -webkit-touch-callout: {prop}; /* iOS Safari */
    -webkit-user-select: {prop}; /* Safari */
        -ms-user-select: {prop}; /* Internet Explorer/Edge */
            user-select: {prop}; /* Chrome, Firefox */'''
