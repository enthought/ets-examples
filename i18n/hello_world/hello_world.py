import os
from gettext import bindtextdomain, gettext as _, textdomain


localedir = os.path.join(
    os.path.dirname(__file__),
    'translations'
)


def init():
    bindtextdomain('hello', localedir)
    textdomain('hello')


def main():
    init()

    # NOTE: a friendly greeting
    print(_("Hello world"))


if __name__ == '__main__':
    main()
