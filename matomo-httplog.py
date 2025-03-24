#!/usr/bin/env python3

from flask import Flask, request, Response
from datetime import datetime
import logging, requests

app = Flask(__name__)

@app.route('/matomo.php', methods=['POST'])
def matomo():
    payload = {
        'idsite': 1,
        'rec': 1,
        'action_name': request.json["route"]["name"],
        'url': 'http://' + request.json["request"]["headers"]["host"]
                         + request.json["request"]["uri"],
        'ua':  request.json["request"]["headers"]["user-agent"],
        'uid': request.json["client_ip"]
    }
    r = requests.get('http://localhost/matomo/matomo.php', params=payload)
    return Response('ok', mimetype='text/plain')


@app.route('/apianalytics.dev', methods=['POST'])
def apianalytics():
    # apianalytics erwartet das Datum als "2024-10-06T21:57:03.186589"
    created_at = request.json["started_at"] / 1000
    created_at = datetime.utcfromtimestamp(created_at).strftime('%Y-%m-%dT%H:%M:%S')

    payload = {
        'api_key': '4313e49c-40d1-43bf-862e-cc739d64445b',
        'framework': 'Flask',
        'privacy_level': 0,
        'requests': [{
            'hostname': request.json["request"]["headers"]["host"],
            'ip_address': request.json["client_ip"],
            'path': request.json["route"]["paths"][0],
            'user_agent': request.json["request"]["headers"]["user-agent"],
            'method': request.json["request"]["method"],
            'status': request.json["response"]["status"],
            'response_time': int(request.json["tries"][0]["balancer_latency_ns"] / 1000),
            'user_id': 'none',
            'created_at': created_at
        }]
    }
    r = requests.post('https://www.apianalytics-server.com/api/log-request', json=payload)
    print(r.text)

    if r.status_code == requests.codes.ok:
        return Response('ok', mimetype='text/plain')
    else:
        return Response('fail', mimetype='text/plain')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
