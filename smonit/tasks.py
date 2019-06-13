from datetime import datetime
from time import sleep

from smonit.services.api import Salt
from smonit.services.api import InfluxDB
from smonit.schema import Data


salt = Salt()
influxdb = InfluxDB()
schema = Data()


def connected():
    status = salt.minions_accepted
    data = schema.default('connected', len(status))

    return influxdb.write_multiple_data(data)


def pending():
    status = salt.minions_pending
    data = schema.default('pending', len(status))

    return influxdb.write_multiple_data(data)


def denied():
    status = salt.minions_denied
    data = schema.default('denied', len(status))

    return influxdb.write_multiple_data(data)


def rejected():
    status = salt.minions_rejected
    data = schema.default('rejected', len(status))

    return influxdb.write_multiple_data(data)


def active(minion):
    success_respond = salt.respond_minion(minion)
    time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    value = 0

    if success_respond:
        value = 1

    data = schema.with_tag('active', value, minion)

    return influxdb.write_multiple_data(data)


def check_changes(minion):
    respond = salt.respond_minion(minion)

    if respond:
        changes_result = salt.changes(minion)
        errors = 0
        success = 0

        if changes_result:
            for identification_id, state in changes_result.items():
                for state_name in state:
                    state_info = state.get(state_name)
                    change_state_out = state_info.get('stdout')
                    change_state_err = state_info.get('stderr')

                    if change_state_out != '':
                        success = 1
                    if change_state_err != '':
                        errors = 1

                    data = schema.changes_minion(identification_id,
                                                 minion,
                                                 state_name,
                                                 errors,
                                                 success)

                    print(data)
                    influxdb.write_multiple_data(data)
    return True
