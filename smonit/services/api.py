import os
import logging
import timeit
from influxdb import InfluxDBClient

try:
    import salt.config
    import salt.client
    import salt.utils
except ImportError:
    raise RuntimeError(
        "You must install salt package to use this service")

from salt.key import Key
from smonit.exceptions import SaltExceptions

log = logging.getLogger(__name__)


class Salt(object):
    def __init__(self):
        self._opts = salt.config.master_config('/etc/salt/master')
        self._lc = salt.client.LocalClient()
        self.keys = Key(self._opts)

    @property
    def get_minions(self):
        return self.keys.list_keys()

    @property
    def minions_accepted(self):
        minions_list = []
        for minion in self.get_minions['minions']:
            if minion:
                minions_list.append(minion)

        return minions_list

    @property
    def minions_pending(self):
        return [minion for minion in self.get_minions['minions_pre']]

    @property
    def minions_rejected(self):
        return [minion for minion in self.get_minions['minions_rejected']]

    @property
    def minions_denied(self):
        return [minion for minion in self.get_minions['minions_denied']]

    def respond_minion(self, minion):
        '''
        :param minion' server name
        '''
        check_respond = self._lc.cmd(minion, 'test.ping', timeout=2)

        for minion, res in check_respond.items():
            if res is True:
                return True
        return

    def cmd(self, minion, function, arg=[], return_key='ret'):
        '''
        :param minion: server name
        :param function: module name
        :param arg: list of parameters or comamnds
        :param return_key: key return. Can be ret or return
        '''
        ret = self._lc.cmd(minion, function, arg, full_return=True)

        if not ret[minion][return_key]:
            log.error('The Salt call failed to return any data')
            raise SaltExceptions()

        return ret

    def states(self, minion, return_key='ret', number=True):
        '''
        :param minion' server name
        :param return_key: key return. Can be ret or return
        :param number: how many states are, Default states name
        '''
        result = self.cmd(minion, 'state.highstate')
        states_list = []

        if result[minion][return_key]:
            for info in result[minion][return_key].values():
                if info['__sls__'] not in states_list:
                    states_list.append(info['__sls__'])

        if number:
            states = len(states_list)
        else:
            states = states_list

        return states

    def _minion_info(self, minion, return_key='ret'):
        '''
        :param minion' server name
        :param return_key: key return. Can be ret or return
        '''
        result = self.cmd(minion, 'state.highstate')
        result = result[minion][return_key]

        if result:
            try:
                values = result.values()
            except AttributeError:
                log.critical(f'ID duplication issues on {minion} minion')
                values = None

        return values

    def changes(self, minion):
        '''
        :param minion: server id connected
        '''
        values = self._minion_info(minion)
        changes_list = {}

        if values:
            for info in values:
                changes = info['changes']

                if len(changes) > 0:
                    if changes['stdout'] != '' or changes['stderr'] != '':
                        changes_list.update({
                            info['__id__']: {
                                info['__sls__']: changes
                            }
                        })

        return changes_list


class InfluxDB(object):
    def __init__(self, endpoint=None, user=None, password=None, database=None):
        if endpoint:
            self.host, self.port = endpoint.split(':')
        else:
            self.host, self.port = os.environ.get('INFLUXDB_ENDPOINT',
                                                  'localhost:8086').split(':')
        self.user = user or os.environ.get('INFLUXDB_USER')
        self.password = password or os.environ.get('INFLUXDB_PASSWORD')
        self.database = database or os.environ.get('INFLUXDB_DB', 'smonit')

    @property
    def _connection(self):
        return InfluxDBClient(self.host,
                              self.port,
                              self.user,
                              self.password,
                              self.database)

    @property
    def list_databases(self):
        return self._connection.get_list_database()

    def create_database(self, database):
        return self._connection.create_database(database)
