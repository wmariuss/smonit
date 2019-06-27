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
        states_changes_list = []
        failure_state_changes = []
        highstate_value = 0
        highstate_issue = 0

        if len(result) > 0:
            if 'disabled' not in result:
                # Set value to 1 if highstate run is enabled
                highstate_value = 1

                for identification_id, states in result.items():
                    for state in states:
                        if state not in states_list:
                            states_list.append(state)

                        state_info = states.get(state)
                        stdout = state_info.get('stdout')
                        stderr = state_info.get('stderr')

                        if stdout != '' or stderr != '':
                            # Add all states with status change. Add even for duplication
                            states_changes_list.append(state)
                        if stderr != '':
                            # Add all states with status failed. For duplication too
                            failure_state_changes.append(state)

                # Add only number of states
                data_number_states = schema.with_tag('number_states', minion, len(states_list))
                influxdb.write_multiple_data(data_number_states)

                # Add number of states with status change
                for state in states_list:
                    changes_number = states_changes_list.count(state)
                    data_number_states_changes = schema.state_changes(minion, state, changes_number)
                    influxdb.write_points(data_number_states_changes)
                    # Add failure changes
                    failure_number = failure_state_changes.count(state)
                    data_number_failure_changes = schema.failure_changes(minion, state, failure_number)
                    influxdb.write_points(data_number_failure_changes)
                    sleep(2)

                if len(failure_state_changes) >= 1:
                    highstate_issue = 1

            data_highstate_issue = schema.with_tag('highstate_issue', minion, highstate_issue)
            influxdb.write_multiple_data(data_highstate_issue)

            data_highstate_disabled = schema.with_tag('highstate_disabled', minion, highstate_value)
            influxdb.write_multiple_data(data_highstate_disabled)
    return
