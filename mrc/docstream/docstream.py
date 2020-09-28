from typing import IO


class DocStream:
    def __init__(self, path):
        try:
            self.__file: IO = open(path, 'r', encoding='utf-8')
        except OSError as os_err:
            print('File can not be opened. ' + str(os_err))
        except ValueError as v_err:
            print('Encoding error. ' + str(v_err))

        next(self.__file)  # skip header

    def __get_document(self):
        for line in self.__file:
            text, label = line[:-3], int(line[-2])
            yield text, label

    def get_minibatch(self, size: int):
        if size <= 0:
            raise ValueError('Batch size can not be less or equal zero.')

        docs, y = [], []

        try:
            for _ in range(size):
                text, label = next(self.__get_document())
                docs.append(text)
                y.append(label)
        except StopIteration:
            return None, None

        return docs, y
