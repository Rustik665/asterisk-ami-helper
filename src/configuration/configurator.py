"""
    Package for work with configuration options from config file
"""
__author__ = 'Fayzullin R.R'
import os
import configparser
from src.constants import CONFIG_FILENAME
from src.db import DB


class Configurator:
    """ Class for work with config-file """

    def __init__(self):
        self._file_path = '{}/config/{}'.format('/'.join(os.path.dirname(__file__).split('/')[:-2]), CONFIG_FILENAME)
        self._log_level = 0
        self._language = 'en'
        self._db = DB()

    @property
    def log_level(self) -> int:
        """ :return log_level """
        return self._log_level

    @property
    def language(self) -> str:
        """ :return program language """
        return self._language

    def read_config(self):
        """ Get config from file """
        config = configparser.ConfigParser()
        config.read(self._file_path)
        if int(config.get("logger", "log_level")) in [0, 1, 2]:
            self._log_level = int(config.get('logger', 'log_level'))
        if config.get('main', 'language'):
            self._language = config.get('main', 'language')

    def read_db(self) -> list:
        """ Get pbx data from DB """
        self._db.check_tables()
        return self._db.get_saved_pbx_credentials()

    def save_pbx_credentials(self, host: str, port: int, username: str, password: str) -> None:
        """ Save pbx credentials """
        self._db.save_pbx_credentials(host, port, username, password)
