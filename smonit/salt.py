
try:
    import salt.client
    import salt.utils
except ImportError:
    raise RuntimeError(
        "You must install salt package to use this service")


class Api(object):
    def __init__(self):
        self._l = salt.client.LocalClient()

    def minion(self, servers='*'):
        minions_list = []

        minions = self._l.cmd(servers, 'test.ping', timeout=1)

        for minion, res in minions.items():
            if minion:
                if res is True:
                    minions_list.append(minion)
        return minions_list
