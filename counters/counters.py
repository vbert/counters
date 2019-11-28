# -*- coding: utf-8 -*-

import sys

# System arguments passed to script
# arg[0] - script name,
# arg[1] - full path for source file with meter readings
try:
    PATH_SRC = sys.argv[1]
except IndexError as err:
    print("IndexError - Brak ścieżki do pliku źródłowego: ", err)
    sys.exit()


def get_src_readings():
    pass


def main():
    # declare variable for system arguments list
    sys_args = sys.argv

    # remove Python script name from args list
    sys_args.pop(0)

    path_src = sys_args[1]


# have interpreter call the main() func
if __name__ == "__main__":
    main()
