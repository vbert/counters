# -*- coding: utf-8 -*-
# © by vbert (wsobczak@gmail.com)
# 2019-11
import os

CONFIG_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_COUNTERS = 'liczniki.dat'
DEFAULT_READINGS = 'sciezka.dat'


def get_readings_path(file_name=DEFAULT_READINGS):
    full_path = os.path.join(CONFIG_PATH, file_name)
    if os.path.isfile(full_path):
        file = open(full_path, 'r')
        path = file.readline()
        return path.strip()
    else:
        return False


def get_counters_ids(file_name=DEFAULT_COUNTERS):
    full_path = os.path.join(CONFIG_PATH, file_name)
    if os.path.isfile(full_path):
        import csv
        data = open(full_path, 'r', encoding='ISO-8859-1')
        reader = csv.reader(data, delimiter=';')
        result = {}
        for col in reader:
            result[col[0]] = col[1]
        return result
    else:
        return False


def test():
    print('Read configs files ...')
