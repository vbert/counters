# -*- coding: utf-8 -*-
# © by vbert (wsobczak@gmail.com)
# 2019-11
import os

DEFAULT_COUNTERS = 'liczniki.dat'
DEFAULT_PATHS = 'sciezki.dat'
TMP_INPUT_FILE = 'tmp-src-utf8.txt'

INPUT_DELIMITER = '|'
INPUT_COLUMNS = ['Data', 'Wejście dod 1', 'Energia', 'Adres']
COL_DATE_READING = 0
COL_METER_READING_1 = 1
COL_METER_READING_2 = 2
COL_ADDRESS = 3
OUTPUT_FILE = 'notesrecrs.sod'
OUTPUT_TPL_START = 'START ODCZYTY;'
OUTPUT_TPL_ROW = ':{place_index},1,{date_reading},2,,,,1,{meter_reading_1},0,2,{meter_reading_2},0;'
OUTPUT_TPL_END = 'KONIEC ODCZYTY;'

'''
START ODCZYTY
:Indeks lokalu,cyfra rodzaju odczytu,data odczytu,ilość odczytów,,,,cyfra porządkowa,stan licznika 1,numer licznika 1,cyfra porządkowa,stan licznika 2,numer licznika2;
KONIEC ODCZYTY
'''


def test():
    print('Read configs file ...')
