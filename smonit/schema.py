from datetime import datetime


class Data(object):
    def __init__(self):
        self.time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')

    def default(self, mesurement, value):
        data = [{
            "measurement": mesurement,
            "time": self.time,
            "fields": {
                "value": value
            }
        }]

        return data

    def with_tag(self, mesurement, value, tag_name):
        data = [{
            "measurement": mesurement,
            "time":  self.time,
            "tags": {
                "host": tag_name
            },
            "fields": {
                "value": value
            }
        }]

        return data

    def changes_minion(self, identification_id, minion, state, errors, success):
        data = [{
            "measurement": "changes",
            "time": self.time,
            "fields": {
                "id_name": identification_id,
                "errors": errors,
                "success": success,
                "state": state,
                "host": minion
            }
        }]

        return data
