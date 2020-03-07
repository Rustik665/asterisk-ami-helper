"""
   Main file of the program
"""
__author__ = 'Fayzullin R.R'

from src.gui import GUI
from src.configuration import Configurator
from src.logger import Logger


class Main:
    """ Main class """

    def __init__(self):
        self.configurator = Configurator()
        self.logger = None
        self.gui = GUI()

    def start(self):
        """ Test function """
        self.configurator.read_config()
        self.logger = Logger(self.configurator.log_level)
        saved_pbx_connections = self.configurator.read_db()

        self.logger.write_log(2, 'Start in {}'.format(__name__))


if __name__ == '__main__':
    """ Start the program """
    Main().start()
