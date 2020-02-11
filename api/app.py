import falcon, json, pprint
from helpers.db_helper import *

class SaveAction:
    def on_post(self, req, resp):
        db = DbHelper()
        data = req.media
        action = data['action']
        dog = data['dog']
        timestamp = data['timestamp']
        row = db.save_action(action, dog, timestamp)
        body = {
           "dog": dog,
    	   "action": action,
           "id": row
        }
        print(body, flush=True)
        print("action", flush=True)
        resp.body = json.dumps(body)

class ListActions:
    def on_get(self, req, resp):
        db = DbHelper()
        list = db.list_actions()
        print(list)
        resp.body = json.dumps(list)

class CORSComponent(object):
    def process_response(self, req, resp, resource, req_succeeded):
        resp.set_header('Access-Control-Allow-Origin', '*')

        if (req_succeeded
            and req.method == 'OPTIONS'
            and req.get_header('Access-Control-Request-Method')
        ):
            # NOTE(kgriffs): This is a CORS preflight request. Patch the
            #   response accordingly.

            allow = resp.get_header('Allow')
            resp.delete_header('Allow')

            allow_headers = req.get_header(
                'Access-Control-Request-Headers',
                default='*'
            )

            resp.set_headers((
                ('Access-Control-Allow-Methods', allow),
                ('Access-Control-Allow-Headers', allow_headers),
                ('Access-Control-Max-Age', '86400'),  # 24 hours
            ))

api = application = falcon.API(middleware=[CORSComponent() ])
# api.add_route('/agile_central', AgileCentralConnector())
api.add_route('/save_action', SaveAction())
api.add_route('/list_actions', ListActions())
