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

    def changes(self, identification_id, minion, state, errors, success):
        data = {
            "measurement": "changes",
            "time": time(),
            "tags": {
                "minion": minion
            },
            "fields": {
                "id_name": identification_id,
                "errors": errors,
                "success": success,
                "state": state,
                "host": minion
            }
        }

        return data
