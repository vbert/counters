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

print(PATH_SRC)
