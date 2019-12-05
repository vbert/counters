# -*- coding: utf-8 -*-
# © by vbert (wsobczak@gmail.com)
# 2019-11
import os
import sys

APP_PATH = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(APP_PATH, 'config')
LIB_PATH = os.path.join(APP_PATH, 'lib')

try:
    import config.config as conf
except ImportError:
    sys.path.append(CONFIG_PATH)
    import config.config as conf

try:
    import lib.tools as tools
except ImportError:
    sys.path.append(LIB_PATH)
    import lib.tools as tools


# def get_src_readings():
#     path = path_to_readings.read()

#     print("\n-----------------------------")
#     print(f"|{path.strip()}|")
#     print("\n-----------------------------")


# def main():
#     get_src_readings()


def main():
    print(f"--[DEBUG]{'-'*41}")
    # print(f"{APP_PATH}")
    # print(f"{CONFIG_PATH}")
    # print(conf.get_readings_path())
    # counters = conf.get_counters_ids()
    # for k, v in counters.items():
    #     print(f"{k} --> {v}")
    src_path = conf.get_readings_path()
    src_file = 'Wielewska-18-08-28 07m11s57 format.txt'

    # data = tools.get_readings(src_path, src_file)
    data = open(os.path.join(src_path, src_file), 'r', encoding='UTF-16LE')
    line = data.readline()

    print('------------------[1]------------------')
    print(line)
    print('------------------[2]------------------')
    separator = data.readline()
    print(len(separator))
    print(separator)
    print('------------------[3]------------------')
    print(data.readline())
    print(data)

    #
    # tools.decode_readings(src_path, src_file)
    #
    # data = open(os.path.join(src_path, src_file), 'r', encoding='ISO-8859-1')
    # readings = data.read()
    # line = data.readline()

    # result = open(os.path.join(src_path, 'result.sod'), 'w', encoding='UTF8')
    # result.write(line.strip())
    # result.close()

    # def get_readings_path(file_name=DEFAULT_READINGS):
    # full_path = os.path.join(CONFIG_PATH, file_name)
    # if os.path.isfile(full_path):
    #     file = open(full_path, 'r')
    #     path = file.readline()
    #     return path.strip()
    # else:
    #     return False
    # result = {}
    # num = 0
    # for line in data:
    #     num += 1
    #     result[f"row-{num}"] = line
    #     # print(line.strip())
    #     # print(f"{'-'*20}")

    # print(f"{result['row-1']}")
    # print(f"{'-'*50}")
    # print(f"{result['row-2']}")
    # print(f"{'-'*50}")
    # print(f"{result['row-5']}")

    # print(f"{'-'*50}")


# have interpreter call the main() func
if __name__ == "__main__":
    main()
