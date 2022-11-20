#
#   ████
#  ░░███
#   ░███   ██████   █████   █████
#   ░███  ███░░███ ███░░   ███░░
#   ░███ ░███ ░░░ ░░█████ ░░█████
#   ░███ ░███  ███ ░░░░███ ░░░░███
#   █████░░██████  ██████  ██████
#  ░░░░░  ░░░░░░  ░░░░░░  ░░░░░░

from lcss.main import run, transpile  # noqa: F401


if __name__ == 'main':
    """
    Command line usage examples:
        $ lcss style.lcss > style.css
        $ lcss style.lcss mixins_dir > style.css

    Preferred usage:
        1) Create default config (lcss_conf.py) by running `lcss` without arguments;
        2) Edit the config and specify in/out files and import mixins module if exists;
        3) Run `lcss` without arguments.

    You can see some examples in `tests` dir.
    """
    run()
