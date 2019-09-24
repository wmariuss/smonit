import json
import falcon


class Index(object):
    def __init__(self):
        pass

    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.body = json.dumps({"service": "smonit"})
