# -*- coding:utf-8 -*-
"""
Project: config
File: /config.py
File Created: 2020-10-26, 20:25:58
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-08-25, 13:56:52
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 - 2022 by vbert
"""
import os

APP_WINDOW_FILE = 'appwindow.ui'

DEFAULT_COUNTERS = 'liczniki.dat'
DEFAULT_PATHS = 'sciezki.dat'
TMP_INPUT_FILE = 'tmp-src-utf8.txt'
DELIMITER_INPUT_FILE = '|'

CONVERSION_TYPES = ['rental', 'analysis', ]

# Conversion parameters
CONVERSION_PARAMETERS = {
    'rental': {
        'delimiter': DELIMITER_INPUT_FILE,
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
        'delimiter': DELIMITER_INPUT_FILE,
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
            'start': 'Adres;Data;Energia;Wejście dod 1;Wejście dod 2;Wejście dod 3;Wejście dod 4',
            'address_as': 'string',
            'row': '{place_address};{date_reading};{energy};{meter_reading_1};{meter_reading_2};{meter_reading_3};{meter_reading_4}',
            'end': ''
        }
    },
}


def test():
    print('Read configs file ...')
