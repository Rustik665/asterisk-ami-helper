"""
    Package for work with internal database
"""
__author__ = 'Fayzullin R.R'
import os
import sqlite3
from src.constants import DB_FILENAME, PBX_TABLE_NAME


class DB:
    """ Class for work with DB """

    def __init__(self):
        self._file_path = '{}/config/{}'.format('/'.join(os.path.dirname(__file__).split('/')[:-2]), DB_FILENAME)
        self._conn = sqlite3.connect(self._file_path)

    def check_tables(self) -> None:
        """ Create tables, if they're not exist """
        cursor = self._conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?", [PBX_TABLE_NAME])
        if not cursor.fetchall():
            cursor.execute("""CREATE TABLE {} (id int primary key,
                                               host text,
                                               port int,
                                               username text,
                                               password text)""".format(PBX_TABLE_NAME))
            self._conn.commit()

    def get_saved_pbx_credentials(self) -> list:
        """ :return credentials of previous saved sessions """
        cursor = self._conn.cursor()
        cursor.execute('SELECT "host", "port", "username", "password" FROM "PBX_LIST"')
        return cursor.fetchall()

    def save_pbx_credentials(self, host: str, port: int, username: str, password: str) -> None:
        """ Save pbx credentials to DB """
        cursor = self._conn.cursor()
        cursor.execute("""INSERT INTO {} (host, port, username, password) 
                          VALUES ('{}', '{}', '{}', '{}')""".format(PBX_TABLE_NAME,
                                                                    host,
                                                                    port,
                                                                    username,
                                                                    password))
        self._conn.commit()
