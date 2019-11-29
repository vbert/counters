# -*- coding: utf-8 -*-
import sys
from config import path_to_readings

# System arguments passed to script
# arg[0] - script name,
# arg[1] - full path for source file with meter readings
# try:
#     PATH_SRC = sys.argv[1]
# except IndexError as err:
#     print("IndexError - Brak ścieżki do pliku źródłowego: ", err)
#     sys.exit()


def get_src_readings():
    path = path_to_readings.read()

    print("\n-----------------------------")
    print(f"|{path.strip()}|")
    print("\n-----------------------------")


def main():
    get_src_readings()


# have interpreter call the main() func
if __name__ == "__main__":
    main()
