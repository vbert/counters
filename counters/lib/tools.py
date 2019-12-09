# -*- coding: utf-8 -*-
# © by vbert (wsobczak@gmail.com)
# 2019-11
import os
import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic

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

Ui_MainWindow, QtBaseClass = uic.loadUiType(
    os.path.join(RES_PATH, conf.QT_CREATOR_FILE))


class ReadingsModel(QtCore.QAbstractListModel):
    def __init_(self, *args, readings=None, **kwargs):
        super(ReadingsModel, self).__init__(*args, **kwargs)
        self.readings = readings or ['one', 'two']

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole:
            file = self.readings[index.row()]
            return file

    # def rowCount(self, index):
    #     return len(self.readings)


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        # self.model = ReadingsModel()
        # self.readingsView.setModel(self.model)
        # Close button
        self.closeButton.pressed.connect(self.close_app)

    def close_app(self):
        self.close()


def run_app():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


def run_app_2():
    src_path = get_readings_path()
    src_file = 'Wielewska-18-08-28 07m11s57 format.txt'
    input_file = os.path.join(src_path, src_file)
    input_file_utf8 = os.path.join(TMP_PATH, conf.TMP_INPUT_FILE)
    decode_readings(input_file, input_file_utf8)
    readings = get_readings(input_file_utf8)
    if readings:
        contents = convert(readings)
        out_path = get_output_path()
        out_file = conf.OUTPUT_FILE
        output_file = os.path.join(out_path, out_file)
        out = open(output_file, mode='w', encoding='UTF-8')
        contents = "\n".join(contents)
        out.write(contents)
        out.close()
    else:
        pass


def get_paths(file_name):
    full_path = os.path.join(CONFIG_PATH, file_name)
    if os.path.isfile(full_path):
        file = open(full_path, 'r')
        return file.readlines()
    else:
        return False


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
    out = open(output_file, mode='w', encoding='UTF-8')
    contents = "\n".join(contents)
    out.write(contents)
    out.close()


def strip_csv_row(row):
    row = list(map(str.strip, row.split(conf.INPUT_DELIMITER)))
    return conf.INPUT_DELIMITER.join(row)


def get_readings(file):
    if os.path.isfile(file):
        import csv
        readings = []
        with open(file) as csvfile:
            reader = csv.DictReader(csvfile, delimiter=conf.INPUT_DELIMITER)
            for line in reader:
                row = {}
                for col in conf.INPUT_COLUMNS:
                    row[col] = line[col]
                readings.append(row)
        return readings
    else:
        return False


def convert(readings):
    contents = []
    contents.append(conf.OUTPUT_TPL_START)
    places_ids = get_places_ids()
    for line in readings:
        address = line[conf.INPUT_COLUMNS[conf.COL_ADDRESS]]
        if address in places_ids:
            args = {
                'place_index': places_ids[address],
                'date_reading': format_date(line[conf.INPUT_COLUMNS[conf.COL_DATE_READING]]),
                'meter_reading_1': format_meter(line[conf.INPUT_COLUMNS[conf.COL_METER_READING_1]]),
                'meter_reading_2': format_meter(line[conf.INPUT_COLUMNS[conf.COL_METER_READING_2]])
            }
            tpl = conf.OUTPUT_TPL_ROW
            row = tpl.format(**args)
            contents.append(row)
    contents.append(conf.OUTPUT_TPL_END + "\n")
    return contents


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


def format_date(date_str):
    from datetime import datetime
    dt = datetime.strptime(date_str, '%y-%m-%d')
    return dt.strftime('%d/%m/%Y')


def format_meter(meter_str):
    return float(meter_str.replace(',', '.')[:-4])


def test():
    print('Read tools file ...')
