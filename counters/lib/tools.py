# -*- coding: utf-8 -*-
# © by vbert (wsobczak@gmail.com)
# 2019-11
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
        # ['Styczeń 2019.txt', 'Luty 2019.txt', 'Marzec 2019.txt', 'Kwiecień 2019 dodatek.txt']
        self.model = QtGui.QStandardItemModel()
        for reading in self.readings:
            self.model.appendRow(QtGui.QStandardItem(reading))
        self.readingsView.setModel(self.model)
        self.readingsView.clicked.connect(self.slot_clicked_item)

        # Export button
        self.file_name = self.readings[self.file_index]
        self.exportButton.clicked.connect(self.convert)
        #lambda: run_convert(self.file_name)

        # Close button
        self.closeButton.clicked.connect(self.close_app)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

    def close_app(self):
        self.close()

    @QtCore.pyqtSlot(QtCore.QModelIndex)
    def slot_clicked_item(self, QModelIndex):
        # self.stk_w.setCurrentIndex(QModelIndex.row())
        self.file_index = QModelIndex.row()

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
    #src_file = 'Wielewska-18-08-28 07m11s57 format.txt'
    src_path = get_readings_path()
    input_file = os.path.join(src_path, src_file)
    input_file_utf8 = os.path.join(TMP_PATH, conf.TMP_INPUT_FILE)
    decode_readings(input_file, input_file_utf8)

    # generate csv file for future analysis
    print(src_file)
    csv_out_name = os.path.splitext(src_file)[0]
    print(csv_out_name)
    csv_out_file_name = '.'.join([os.path.splitext(src_file)[0], 'csv'])
    print(csv_out_file_name)

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
        message = 'Konwersja zakończona pomyślnie.'
    else:
        message = 'Konwersja nie powiodła się.'
    return message


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


def get_readings_files():
    readings_path = get_readings_path()
    files_list = [f for f in os.listdir(readings_path) if os.path.isfile(
        os.path.join(readings_path, f)) and f.endswith('.txt')]
    return sorted(files_list, key=str.casefold, reverse=True)


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
        with open(file, encoding='UTF-8') as csvfile:
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


def test(value):
    print('Read tools file ...')
    print('Przekazana wartość: {val}'.format(val=value))
    return True
