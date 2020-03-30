"""
   Main file of the program
"""
__author__ = 'Fayzullin R.R'

from src.gui import MainGUI, LoginGUI
from src.configuration import Configurator
from src.logger import Logger
from src.asterisk_connector import Asterisk


class Main:
    """ Main class """

    def __init__(self):
        self.configurator = Configurator()
        self.logger = None
        self.login_gui = LoginGUI()
        self.main_gui = None
        self.asterisk = None

    def start(self):
        """ Test function """
        self.configurator.read_config()
        self.logger = Logger(self.configurator.log_level)
        saved_pbx_connections = self.configurator.read_db()

        self.logger.write_log(2, 'Start in {}'.format(__name__))

        self.asterisk = self.login_gui.login_window(saved_pbx_connections)
        self.main_gui = MainGUI()
        self.main_gui.do_something(self.asterisk)

        self.asterisk.connection.close()


if __name__ == '__main__':
    """ Start the program """
    Main().start()
