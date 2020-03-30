"""
    Package for work with GUI-interface of program
"""
__author__ = 'Fayzullin R.R'

from multiprocessing import Process

import gettext
from tkinter import *
from src.asterisk_connector.asterisk import Asterisk
from src.constants import PROGRAM_NAME, DEFAULT_WINDOW_SIZE, AMI_DEFAULT_PORT

gettext.install('messages', '../static/localization')


class MainGUI:
    """ Class for work with Main window """

    def __init__(self):
        self._window = Tk()
        self._window.title(PROGRAM_NAME)
        self._window.resizable(False, False)
        self._wm = 1  # width multiplier
        self._hm = 1  # height multiplier
        self.width = DEFAULT_WINDOW_SIZE[0]
        self.height = DEFAULT_WINDOW_SIZE[1]

    def _set_window_geometry(self, w_m: float = None, h_m: float = None) -> None:
        """ Define current screen resolution and set login window dimensions """
        width_m, height_m = 1, 1
        if w_m and h_m:
            width_m = w_m
            height_m = h_m
        if isinstance(self, LoginGUI):
            width_m, height_m = 0.7, 0.7

        self._wm = (self._window.winfo_screenwidth() / 2.4) / self.width
        self._hm = (self._window.winfo_screenheight() / 2) / self.height
        self.width = round(self.width * self._wm * width_m)
        self.height = round(self.height * self._hm * height_m)
        screen_center = round(self._window.winfo_screenwidth() / 2 - self.width / 2), \
            round(self._window.winfo_screenheight() / 2 - self.height / 2)
        self._window.geometry('{}x{}+{}+{}'.format(self.width, self.height, screen_center[0], screen_center[1]))

    def do_something(self, asterisk: Asterisk) -> None:
        """ Just for educational purposes """
        print('in do_something')
        self._set_window_geometry()

        events = Text(self._window, width=round(20 * self._wm), bd=1)
        events.grid(column=0, row=1, sticky=NSEW)
        events.insert(END, 'test!')

        proc = Process(target=self._window.mainloop)
        proc.start()
        proc.join()

        # self._window.mainloop()

        data = b''
        tmp = asterisk.connection.recv(1024)
        while tmp:
            data += tmp
            print(data.decode('utf-8'))
            tmp = asterisk.connection.recv(1024)
            events.insert(END, '{}\r\n'.format(data.decode('utf-8')))
        print(data.decode('utf-8'))


class LoginGUI(MainGUI):
    """ Class for work with Login window """

    def __init__(self):
        super().__init__()
        self._asterisk = None

    def _connect_button(self, hostname, port, login, password):
        """ Process connect button pressing """
        hostname = hostname.get()
        port = port.get() if port.get() else AMI_DEFAULT_PORT
        login = login.get()
        password = password.get()
        if not (hostname and login and password):
            notification_window = Toplevel(self._window)
            notification_window.grab_set()
            notification_window.title('Ошибка')
            screen_center = round(self._window.winfo_screenwidth() / 2 - self.width / 5), \
                round(self._window.winfo_screenheight() / 2 - self.height / 5)
            notification_window.geometry('+{}+{}'.format(screen_center[0], screen_center[1]))
            notification_window.resizable(False, False)
            return
        self._asterisk = Asterisk(hostname, port, login, password).connect()
        self._window.destroy()

    def login_window(self, saved_pbx_connections: list) -> Asterisk:
        """ Login window """
        self._set_window_geometry()

        labels_params = {"padx": round(7*self._wm), "pady": round(3*self._wm),
                         "ipady": round(1*self._wm), "sticky": "w"}
        entries_params = {"padx": round(7*self._wm), "ipadx": round(1*self._wm), "ipady": round(1*self._wm)}

        hostname_label = Label(self._window, text=_("Hostname"))
        hostname_label.grid(column=0, row=0, **labels_params)
        hostname = Entry(self._window, width=round(20*self._wm), bd=1)
        hostname.grid(column=0, row=1, **entries_params)

        port_label = Label(self._window, text=_("AMI port"))
        port_label.grid(column=1, row=0, **labels_params)
        port = Entry(self._window, width=round(20*self._wm), bd=1)
        port.grid(column=1, row=1, **entries_params)

        login_label = Label(self._window, text=_("Login"))
        login_label.grid(column=0, row=2, **labels_params)
        login = Entry(self._window, width=round(20*self._wm), bd=1)
        login.grid(column=0, row=3, **entries_params)

        password_label = Label(self._window, text=_("Password"))
        password_label.grid(column=1, row=2, **labels_params)
        password = Entry(self._window, width=round(20*self._wm), bd=1, show="*")
        password.grid(column=1, row=3, **entries_params)

        conn_button = Button(self._window, text=_("Connect"), bd=1, width=round(12*self._wm),
                             command=lambda: self._connect_button(hostname, port, login, password))
        conn_button.grid(column=3, row=1, **entries_params)

        last_connections_label = Label(self._window, text=_("Last connections"))
        last_connections_label.grid(column=0, row=4, padx=round(7*self._wm), pady=round(7*self._wm))

        # for line, record in enumerate(saved_pbx_connections):
        #     for i in range(4):
        #         label = Label(self._window, text=record[i+1])
        #         label.grid(column=i, row=line+5)
        self._window.mainloop()
        return self._asterisk

