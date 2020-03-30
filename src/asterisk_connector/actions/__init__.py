"""
    Classes for Actions
"""
__author__ = 'Fayzullin R.R'


def _append_action_id_if_need(action: str, action_id: int) -> str:
    """ Append field ActionID with it's value """
    if action_id:
        return '{}{}\n\n'.format(action, action_id)
    else:
        return '{}\n'.format(action)


class BaseEvent:
    """ Base class for actions """

    def __init__(self, action_id: int = None):
        self.action_id = action_id
        self.action_data = None

    def data(self) -> bytes:
        """ Return bytes-data to send into asterisk """
        return _append_action_id_if_need(self.action_data, self.action_id).encode('utf-8')


class Login(BaseEvent):
    """ Class for action Login """

    def __init__(self, username: str, password: str, action_id: int = None):
        super().__init__(action_id)
        self._action = 'Login'
        self._username = username
        self._password = password
        self.action_data = 'Action: {}\nUsername: {}\nSecret: {}\n'.format(self._action, self._username, self._password)

