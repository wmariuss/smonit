from os import path, mkdir
from datetime import datetime
from time import sleep
from tinydb import TinyDB, Query

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


def respond_minion_db(minion):
    db_path = '/etc/salt/smonit'
    success_respond = salt.respond_minion(minion)
    response = False

    if not path.isdir(db_path):
        mkdir(db_path)

    if success_respond:
        response = True

    db = TinyDB(f'{db_path}/db.json')
    host_query = Query()
    check_minion = db.search(host_query.host == minion)

    if len(check_minion) < 1:
        db.insert({'host': minion, 'response': response})
    else:
        db.update({'response': response}, host_query.host == minion)

    return


def respond_minion():
    db_path = '/etc/salt/smonit/db.json'

    if path.isfile(db_path):
        db = TinyDB(db_path)
        response_query = Query()

        check_response = db.search(response_query.response == 1)
        check_not_response = db.search(response_query.response == 0)

        count_minions_response = 0
        count_minions_not_response = 0

        if len(check_response) >= 1:
            count_minions_response = len(check_response)
        if len(check_not_response) >= 1:
            count_minions_not_response = len(check_not_response)

        data_count_response = schema.default('total_response', count_minions_response)
        influxdb.write_multiple_data(data_count_response)

        data_count_not_response = schema.default('total_not_response', count_minions_not_response)
        influxdb.write_multiple_data(data_count_not_response)

        for data in db:
            response = data.get('response')
            host = data.get('host')

            data_response = schema.responding('response', host, response)
            influxdb.write_multiple_data(data_response)

    return


def check_changes(minion):
    respond = salt.respond_minion(minion)

    if respond:
        result = salt.changes(minion)
        states_list = []
        states_changes_list = []
        failure_state_changes = []
        time_list = []

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
                            # Add all states with status change. Add duplication
                            states_changes_list.append(state)
                            time_list.append(state_info.get('time'))
                        if stderr != '':
                            # Add all states with status failed. Add duplication
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

            # Show if highstate run has some failure changes
            data_highstate_issue = schema.with_tag('highstate_issue', minion, highstate_issue)
            influxdb.write_multiple_data(data_highstate_issue)

            # Show the total number of failure changes
            data_total_failure_number = schema.with_tag('total_failure_changes', minion, len(failure_state_changes))
            influxdb.write_multiple_data(data_total_failure_number)

            # Show the total number of changes
            data_total_changes = schema.with_tag('total_changes', minion, len(states_changes_list))
            influxdb.write_multiple_data(data_total_changes)

            # Show if highstate is disabled
            data_highstate_disabled = schema.with_tag('highstate_disabled', minion, highstate_value)
            influxdb.write_multiple_data(data_highstate_disabled)

            # Add duration time for highstate run
            duration_time = schema.with_tag('highstate_duration', minion, sum(time_list))
            influxdb.write_multiple_data(duration_time)
    return
