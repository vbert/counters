def read(file_name='config/sciezka.dat'):
    file = open(file_name, 'r')
    path = file.readline()
    return path


def test():
    print('Path to readings...1, 2')
