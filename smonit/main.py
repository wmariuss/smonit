import falcon
import logging
import pprint

from smonit.tasks import connected, pending, denied, rejected, respond
from smonit.tasks import check_changes
from smonit.views import Index

from smonit.services.api import Salt, InfluxDb

influx = InfluxDb()

# print(influx.list_databases)
# print(influx.drop_database('smonit'))
# print(influx.create_database('smonit'))

connected()
pending()
denied()
rejected()
respond('saltd')
print(check_changes('saltd'))

# pprint.pprint(influx.query('select * from highstate_disabled'))

salt = Salt()
# minions = salt.minions_accepted
minions = ['saltd']
# for minion in minions:
#     pprint.pprint(salt.cmd(minion, 'state.highstate'))
#     pprint.pprint(salt.changes(minion))


app = falcon.API()
app.add_route('/', Index())
