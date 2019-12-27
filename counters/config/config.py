# -*- coding: utf-8 -*-
# © by vbert (wsobczak@gmail.com)
# 2019-11
import os

APP_WINDOW_FILE = 'appwindow.ui'

DEFAULT_COUNTERS = 'liczniki.dat'
DEFAULT_PATHS = 'sciezki.dat'
TMP_INPUT_FILE = 'tmp-src-utf8.txt'

# Conversion parameters
CONVERSION_PARAMETERS = {
    'rental': {
        'delimiter': '|',
        'columns': {
            'names': ['Data', 'Wejście dod 1', 'Energia', 'Adres'],
            'indexes': {
                'date': 0,
                'reading_1': 1,
                'reading_2': 2,
                'address': 3
            }
        },
        'file_name': 'notesrecrs.sod',
        'template': {
            'start': 'START ODCZYTY;',
            'address_as': 'index',
            'row': ':{place_index},1,{date_reading},2,,,,1,{meter_reading_1},0,2,{meter_reading_2},0;',
            'end': 'KONIEC ODCZYTY;'
        }
    },
    'analysis': {
        'delimiter': '|',
        'columns': {
            'names': ['Adres', 'Data', 'Energia', 'Wejście dod 1', 'Wejście dod 2', 'Wejście dod 3', 'Wejście dod 4'],
            'indexes': {
                'address': 0,
                'date': 1,
                'energy': 2,
                'reading_1': 3,
                'reading_2': 4,
                'reading_3': 5,
                'reading_4': 6
            }
        },
        'part_path': 'excel',
        'template': {
            'start': 'Adres,Data,Energia,Wejście dod 1,Wejście dod 2,Wejście dod 3,Wejście dod 4',
            'address_as': 'string',
            'row': '{place_address},{date_reading},{energy},{meter_reading_1},{meter_reading_2},{meter_reading_3},{meter_reading_4}',
            'end': ''
        }
    },
}
# Rental
# INPUT_RENTAL_DELIMITER = '|'
# INPUT_RENTAL_COLUMNS = ['Data', 'Wejście dod 1', 'Energia', 'Adres']
# COL_RENTAL_DATE_READING = 0
# COL_RENTAL_METER_READING_1 = 1
# COL_RENTAL_METER_READING_2 = 2
# COL_RENTAL_ADDRESS = 3
# OUTPUT_RENTAL_FILE = 'notesrecrs.sod'
# OUTPUT_RENTAL_TPL_START = 'START ODCZYTY;'
# OUTPUT_RENTAL_TPL_ROW = ':{place_index},1,{date_reading},2,,,,1,{meter_reading_1},0,2,{meter_reading_2},0;'
# OUTPUT_RENTAL_TPL_END = 'KONIEC ODCZYTY;'

# Analysis
# INPUT_ANALYSIS_DELIMITER = '|'
# INPUT_ANALYSIS_COLUMNS = ['Adres', 'Data', 'Energia', 'Wejście dod 1', 'Wejście dod 2', 'Wejście dod 3', 'Wejście dod 4']
# COL_ANALYSIS_ADDRESS = 0
# COL_ANALYSIS_DATE_READING = 1
# COL_ANALYSIS_ENERGY = 2
# COL_ANALYSIS_METER_READING_1 = 3
# COL_ANALYSIS_METER_READING_2 = 4
# COL_ANALYSIS_METER_READING_3 = 5
# COL_ANALYSIS_METER_READING_4 = 6
# OUTPUT_ANALYSIS_PART_PATH = 'excel'
# OUTPUT_ANALYSIS_TPL_START = 'Adres,Data,Energia,Wejście dod 1,Wejście dod 2,Wejście dod 3,Wejście dod 4'
# OUTPUT_ANALYSIS_TPL_ROW = '{place_address},{date_reading},{energy},{meter_reading_1},{meter_reading_2},{meter_reading_3},{meter_reading_4}'


def test():
    print('Read configs file ...')
