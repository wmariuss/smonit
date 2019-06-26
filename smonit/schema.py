from smonit.utils import time


class Data(object):
    def __init__(self):
        pass

    def default(self, mesurement, value):
        data = [{
            "measurement": mesurement,
            "time": time(),
            "fields": {
                "value": value
            }
        }]

        return data

    def with_tag(self, table_name, tag, value):
        data = [{
            "measurement": table_name,
            "time": time(),
            "tags": {
                "host": tag
            },
            "fields": {
                "value": value
            }
        }]

        return data

    def responding(self, mesurement, tag, minion, value):
        data = [{
            "measurement": mesurement,
            "time": time(),
            "tags": {
                "active": tag
            },
            "fields": {
                "minion": minion,
                "value": value
            }
        }]

        return data

    def state_changes(self, minion, state, value):
        data = [{
            "measurement": "state_changes",
            "time": time(),
            "tags": {
                "minion": minion
            },
            "fields": {
                "state": state,
                "changes": value
            }
        }]

        return data

    def failure_changes(self, minion, state, value):
        data = [{
            "measurement": "failure_states",
            "time": time(),
            "tags": {
                "minion": minion
            },
            "fields": {
                "state": state,
                "failure": value
            }
        }]

        return data
