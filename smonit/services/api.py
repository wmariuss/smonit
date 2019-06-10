import logging

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

    def changes(self, minion, return_key='ret'):
        '''
        :param minion' server name
        :param return_key: key return. Can be ret or return
        '''
        result = self.cmd(minion, 'state.highstate')
        changes_list = {}
        result = result[minion][return_key]

        if result:
            try:
                values = result.values()
            except AttributeError:
                log.critical(f'No salt data received for {minion} minion. Could be some issues about ID duplications')
            else:
                for info in values:
                    state = info['__sls__']
                    declaration_id = info['__id__']
                    changes = info['changes']

                    if len(changes) > 0:
                        change_ids_list = []
                        failed_change_ids_list = []
                        no_changes_ids_list = []

                        if changes['stdout'] != '':
                            if declaration_id not in change_ids_list:
                                change_ids_list.append(declaration_id)
                        else:
                            if declaration_id not in failed_change_ids_list:
                                failed_change_ids_list.append(declaration_id)
                    else:
                        if declaration_id not in no_changes_ids_list:
                            no_changes_ids_list.append(declaration_id)

                    # state name and the list of IDs declaration
                    changes_list.update({
                        state: {
                            'success': change_ids_list,
                            'errors': failed_change_ids_list,
                            'no_changes': no_changes_ids_list
                        }
                    })

        return changes_list
