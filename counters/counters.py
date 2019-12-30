# -*- coding: utf-8 -*-
# © by vbert (wsobczak@gmail.com)
# 2019-11
import os
import sys

APP_PATH = os.path.dirname(os.path.abspath(__file__))

try:
    import lib.tools as tools
except ImportError:
    sys.path.append(os.path.join(APP_PATH, 'lib'))
    import lib.tools as tools


def main():
    tools.run()


# have interpreter call the main() func
if __name__ == "__main__":
    main()
