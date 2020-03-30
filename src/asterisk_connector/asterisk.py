"""
    Package for work with asterisk
"""
__author__ = 'Fayzullin R.R'

import socket
import src.asterisk_connector.actions as actions


class Asterisk:
    """ Class for work with asterisk """

    def __init__(self, host: str, port: int, login: str, password: str):
        self._host = host
        self._port = port
        self._login = login
        self._password = password
        self.connection = None
        self.is_active = False

    def connect(self) -> object:
        """ Connect to asterisk AMI interface """
        self.connection = socket.socket()
        self.connection.connect((self._host, self._port))
        self.connection.send(actions.Login('user', 'pass', 12345).data())
        data = self.connection.recv(128).decode('utf-8')
        data += self.connection.recv(128).decode('utf-8')
        print('data: {}\r\n'.format(data))
        if 'Authentication accepted' in data:
            self.is_active = True
            return self
        return None

    def disconnect(self) -> None:
        """ Disconnect from asterisk AMI interface """
        self.connection.close()
