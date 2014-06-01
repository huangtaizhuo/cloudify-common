########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

__author__ = 'idanmo'

import requests

from cloudify_rest_client.blueprints import BlueprintsClient
from cloudify_rest_client.deployments import DeploymentsClient
from cloudify_rest_client.executions import ExecutionsClient
from cloudify_rest_client.exceptions import *


class NodesClient(object):

    def __init__(self, rest_client):
        self.rest_client = rest_client


class NodeInstancesClient(object):

    def __init__(self, rest_client):
        self.rest_client = rest_client


class ManagerClient(object):

    def __init__(self, rest_client):
        self.rest_client = rest_client


class Client(object):

    def __init__(self, host, port=80):
        self.port = port
        self.host = host
        self.url = 'http://{0}:{1}'.format(host, port)

    def _raise_client_error(self, response):
        print 'error:', response.status_code, response.content
        raise CloudifyClientError()

    def get(self, uri, expected_status_code=200):
        request_url = '{0}{1}'.format(self.url, uri)
        response = requests.get(request_url,
                                headers={'Content-type': 'application/json'})
        if response.status_code != expected_status_code:
            self._raise_client_error(response)
        return response.json()


class RestClient(object):

    def __init__(self, host, port=80):
        self._client = Client(host, port)
        self.blueprints = BlueprintsClient(self._client)
        self.deployments = DeploymentsClient(self._client)
        self.executions = ExecutionsClient(self._client)


if __name__ == '__main__':
    client = RestClient('15.126.223.101')
    result = client.blueprints.list()
    print 'blueprints:', result

    result = client.deployments.list()
    print 'deployments:', result

    result = client.executions.list('hello')
    print 'executions:', result

    result = client.deployments.list_workflows('hello')
    print 'workflows:', result

    for workflow in result.workflows:
        print 'workflow:', workflow