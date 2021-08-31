# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from flask import Flask, request, Response, abort
import requests
import openstack

app = Flask(__name__)

app.config.from_pyfile('/etc/swift-proxy/config.cfg')

CONN = None
TOKEN = None


def auth():
    global CONN
    global TOKEN
    CONN = openstack.connect(f"{app.config['CLOUD_NAME']}")
    TOKEN = CONN.authorize()


def query(path):
    req_headers = dict()
    req_headers['X-Auth-Token'] = TOKEN
    url = f"{app.config['SITE_NAME']}{path}"
    app.logger.debug(f'Querying {url}')
    resp = requests.get(url, headers=req_headers)
    return resp


@app.route('/<path:path>', methods=['GET'])
def proxy(path):
    if request.method == "GET":
        resp = query(path)
        if resp.status_code == 401:
            app.logger.debug('Request returned 401. Renew the auth and retry')
            auth()
            resp = query(path)
        excluded_headers = ["content-encoding", "content-length",
                            "transfer-encoding", "connection"]
        headers = [
            (name, value) for (name, value) in
            resp.raw.headers.items() if name.lower() not in excluded_headers
        ]
        response = Response(resp.content, resp.status_code, headers)
    else:
        abort(401)
    return response


application = app


if __name__ == '__main__':
    app.run()
