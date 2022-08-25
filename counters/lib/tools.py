# -*- coding:utf-8 -*-
"""
Project: lib
File: /tools.py
File Created: 2020-10-26, 20:25:58
Author: Wojciech Sobczak (wsobczak@gmail.com)
-----
Last Modified: 2022-08-25, 13:55:46
Modified By: Wojciech Sobczak (wsobczak@gmail.com)
-----
Copyright © 2021 - 2022 by vbert
"""
import os
import sys
from PyQt5 import uic
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets

APP_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_PATH = os.path.join(APP_PATH, 'config')
LIB_PATH = os.path.join(APP_PATH, 'lib')
RES_PATH = os.path.join(APP_PATH, 'resources')
TMP_PATH = os.path.join(APP_PATH, 'tmp')

try:
    import config.config as conf
except ImportError:
    sys.path.append(CONFIG_PATH)
    import config.config as conf

ui_path = os.path.join(RES_PATH, conf.APP_WINDOW_FILE)
Ui_MainWindow, QtBaseClass = uic.loadUiType(ui_path)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.file_index = -1

        # Readings files view
        self.readings = get_readings_files()
        self.model = QtGui.QStandardItemModel()
        for reading in self.readings:
            self.model.appendRow(QtGui.QStandardItem(reading))
        self.readingsView.setModel(self.model)
        self.readingsView.clicked.connect(self.slot_clicked_item)

        # Export button
        self.file_name = self.readings[self.file_index]
        self.exportButton.clicked.connect(self.convert)

        # Close button
        self.closeButton.clicked.connect(self.close_app)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def close_app(self):
        self.close()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def slot_clicked_item(self, QModelIndex):
        self.file_index = QModelIndex.row()
        self.file_name = self.readings[self.file_index]

    @QtCore.pyqtSlot()
    def convert(self):
        response = run_convert(self.file_name)
        self.statusBar.showMessage(response)


def run():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


def run_convert(src_file):
    input_path = get_readings_path()
    output_path = get_output_path()
    input_file = os.path.join(input_path, src_file)

    response_convert = {}
    for conversion in conf.CONVERSION_TYPES:
        input_file_utf8 = os.path.join(TMP_PATH, conf.TMP_INPUT_FILE)
        decode_readings(input_file, input_file_utf8)
        response_convert[conversion] = globals()[f"convert_for_{conversion}"](
            src_file, input_file_utf8, input_path, output_path, conversion)

    errors = 0
    for conversion in conf.CONVERSION_TYPES:
        if response_convert[conversion] == False:
            errors += 1

    if errors == 0:
        message = 'Konwersja zakończona pomyślnie.'
    else:
        message = 'Konwersja nie powiodła się.'
    return message


def convert_for_rental(src_file, input_file_utf8, input_path, output_path, conversion):
    param = conf.CONVERSION_PARAMETERS[conversion]
    readings = get_readings(input_file_utf8, param['columns']['names'])
    output_file = os.path.join(output_path, param['file_name'])

    contents = []
    contents.append(param['template']['start'])
    places_ids = get_places_ids()
    date_col = param['columns']['indexes']['date']
    reading_1_col = param['columns']['indexes']['reading_1']
    reading_2_col = param['columns']['indexes']['reading_2']
    address_col = param['columns']['indexes']['address']
    for line in readings:
        address = line[param['columns']['names'][address_col]]
        if address in places_ids:
            args = {
                'place_index': places_ids[address],
                'date_reading': format_date(line[param['columns']['names'][date_col]]),
                'meter_reading_1': format_meter(line[param['columns']['names'][reading_1_col]]),
                'meter_reading_2': format_meter(line[param['columns']['names'][reading_2_col]])
            }
            tpl = param['template']['row']
            row = tpl.format(**args)
            contents.append(row)
    contents.append(param['template']['end'] + "\n")

    out = open(output_file, mode='w', encoding='UTF-8')
    out.write("\n".join(contents))
    out.close()
    return True


def convert_for_analysis(src_file, input_file_utf8, input_path, output_path, conversion):
    param = conf.CONVERSION_PARAMETERS[conversion]
    readings = get_readings(input_file_utf8, param['columns']['names'])
    output_file = os.path.join(input_path, param['part_path'], '.'.join([os.path.splitext(src_file)[0], 'csv']))

    contents = []
    contents.append(param['template']['start'])
    address_col = param['columns']['indexes']['address']
    date_col = param['columns']['indexes']['date']
    energy_col = param['columns']['indexes']['energy']
    reading_1_col = param['columns']['indexes']['reading_1']
    reading_2_col = param['columns']['indexes']['reading_2']
    reading_3_col = param['columns']['indexes']['reading_3']
    reading_4_col = param['columns']['indexes']['reading_4']
    for line in readings:
        address = line[param['columns']['names'][address_col]]
        args = {
            'place_address': address,
            'date_reading': format_date(line[param['columns']['names'][date_col]], '%Y-%m-%d'),
            'energy': format_meter(line[param['columns']['names'][energy_col]], False),
            'meter_reading_1': format_meter(line[param['columns']['names'][reading_1_col]], False),
            'meter_reading_2': format_meter(line[param['columns']['names'][reading_2_col]], False),
            'meter_reading_3': format_meter(line[param['columns']['names'][reading_3_col]], False),
            'meter_reading_4': format_meter(line[param['columns']['names'][reading_4_col]], False)
        }
        tpl = param['template']['row']
        row = tpl.format(**args)
        contents.append(row)
    contents.append("\n")

    out = open(output_file, mode='w', encoding='UTF-8')
    out.write("\n".join(contents))
    out.close()
    return True


def get_paths(file_name):
    full_path = os.path.join(CONFIG_PATH, file_name)
    if os.path.isfile(full_path):
        file = open(full_path, 'r')
        return file.readlines()
    else:
        return False


def get_readings_files():
    readings_path = get_readings_path()
    files_list = [f for f in os.listdir(readings_path) if os.path.isfile(
        os.path.join(readings_path, f)) and f.endswith('.txt')]
    return sorted(files_list, key=str.casefold, reverse=True)


def get_readings_path(file_name=conf.DEFAULT_PATHS):
    paths = get_paths(file_name)
    return paths[0].strip()


def get_output_path(file_name=conf.DEFAULT_PATHS):
    paths = get_paths(file_name)
    return paths[1].strip()


def decode_readings(input_file, output_file):
    src = open(input_file, mode='r', encoding='UTF-16LE')
    contents = src.readlines()
    src.close()
    # Deletes row 2 with a horizontal line between the header and content
    contents.pop(1)
    # Remove leading and trailing spaces
    contents = list(map(strip_csv_row, contents))

    tmp_contents = []

    lp = 1

    for row in contents:
        row = list(map(str.strip, row.split(conf.DELIMITER_INPUT_FILE)))

        print(f'# {lp}')
        print(row)
        print('-'*30)
        lp += 1

        # if row[1] != 'NULL':
        tmp_contents.append(conf.DELIMITER_INPUT_FILE.join(row))

    out = open(output_file, mode='w', encoding='UTF-8')
    out.write("\n".join(tmp_contents))
    out.close()


def strip_csv_row(row):
    row = list(map(str.strip, row.split(conf.DELIMITER_INPUT_FILE)))
    return conf.DELIMITER_INPUT_FILE.join(row)


def get_readings(file, columns_list):
    if os.path.isfile(file):
        import csv
        readings = []
        with open(file, encoding='UTF-8') as csvfile:
            reader = csv.DictReader(
                csvfile, delimiter=conf.DELIMITER_INPUT_FILE)
            for line in reader:
                row = {}
                for col in columns_list:
                    row[col] = line[col]
                readings.append(row)
        return readings
    else:
        return False


def get_places_ids(file_name=conf.DEFAULT_COUNTERS):
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


def format_date(date_str, format_out='%d/%m/%Y'):
    from datetime import datetime
    if date_str == '':
        return ''
    else:
        dt = datetime.strptime(date_str, '%y-%m-%d')
        return dt.strftime(format_out)


def format_meter(meter_str, separator=True):
    if meter_str == '':
        return ''
    else:
        if separator == True:
            return float(meter_str.replace(',', '.')[:-4])
        else:
            return meter_str[:-4]


def test(value):
    print('Read tools file ...')
    print('Przekazana wartość: {val}'.format(val=value))
    return True


def print_debug(*args):
    print(f"==[DEBUG]{'='*41}")
    if len(args) > 0:
        for a in args:
            print(a)
            print(f"{'-'*50}")
    else:
        print('     Brak argumentów')
    print(f"{'='*43}[END]==")
