"""
    Logger Package
"""
__author__ = 'Fayzullin R.R'
import os
from datetime import datetime
from src.constants import LOG_FILENAME, LOG_LEVELS_STR


class Logger:
    """ Class Logger """

    def __init__(self, level: int):
        # TODO тут надо сделать проверку размера лог-файла. Если слишком большой - старый нужно заархивировать
        self._file_path = '{}/log/{}'.format('/'.join(os.path.dirname(__file__).split('/')[:-2]), LOG_FILENAME)
        self._log_level = level

    @property
    def file_path(self) -> str:
        """ :return filepath of log-file """
        return self._file_path

    def write_log(self, level: int, message: str) -> None:
        """ Writes message with loglevel to log-file """
        if level > self._log_level:
            return
        record_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        with open(self._file_path, 'a') as file:
            file.write('[{}] [{}] {}\r\n'.format(record_time, LOG_LEVELS_STR[level], message))
