from datetime import datetime
from time import sleep

from smonit.services.api import Salt
from smonit.services.api import InfluxDb
from smonit.schema import Data


salt = Salt()
influxdb = InfluxDb()
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


def respond(minion):
    success_respond = salt.respond_minion(minion)
    tag = False
    value = 1

    if success_respond:
        tag = True

    data = schema.responding('respond', tag, minion, value)

    return influxdb.write_multiple_data(data)


def check_changes(minion):
    respond = salt.respond_minion(minion)

    if respond:
        result = salt.changes(minion)
        states_list = []
        data_list = []

        if result:
            for identification_id, states in result.items():
                for state in states:
                    if state not in states_list:
                        states_list.append(state)

                    state_info = states.get(state)
                    change_state_out = state_info.get('stdout')
                    change_state_err = state_info.get('stderr')

                    print(change_state_out)

                    # if change_state_out != '':
                    #     success = 1
                    # if change_state_err != '':
                    #     errors = 1

                    # data = schema.changes(identification_id,
                    #                       minion,
                    #                       state_name,
                    #                       errors,
                    #                       success)
                    # data_list.append(data)
        # Add number of states
        data_number_states = schema.with_tag('number_states', minion, len(states_list))
        influxdb.write_multiple_data(data_number_states)
    return
