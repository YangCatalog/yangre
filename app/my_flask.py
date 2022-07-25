# Copyright The IETF Trust 2022, All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__author__ = 'Slavomir Mazur'
__copyright__ = 'Copyright The IETF Trust 2022, All Rights Reserved'
__license__ = 'Apache License, Version 2.0'
__email__ = 'slavomir.mazur@pantheon.tech'

from urllib.error import URLError

import config  # pyright: ignore
from flask import Flask, request
from piwikapi.tests.request import FakeRequest
from piwikapi.tracking import PiwikTracker


class MyFlask(Flask):
    def __init__(self, import_name: str):
        super(MyFlask, self).__init__(import_name)
        self.config.from_object('config')

    def preprocess_request(self):
        super().preprocess_request()
        if '/ping' in request.path:
            return

        site_id = getattr(config, 'MATOMO_SITE_ID')
        if not site_id:
            return
        client_ip = request.remote_addr

        headers_dict = get_headers_dict(request)
        try:
            record_analytic(headers_dict, client_ip)
        except URLError:
            pass


def get_headers_dict(req) -> dict:
    keys_to_serialize = [
        'HTTP_USER_AGENT',
        'REMOTE_ADDR',
        'HTTP_REFERER',
        'HTTP_ACCEPT_LANGUAGE',
        'SERVER_NAME',
        'PATH_INFO',
        'QUERY_STRING',
    ]
    data = {
        'HTTPS': req.is_secure
    }
    for key in keys_to_serialize:
        if key in req.headers.environ:
            data[key] = req.headers.environ[key]
    return data


def record_analytic(headers: dict, client_ip: str) -> None:
    """ Send analytics data to Piwik/Matomo """
    # Use "FakeRequest" because we had to serialize the real request
    fake_request = FakeRequest(headers)

    piwik_tracker = PiwikTracker(config.MATOMO_SITE_ID, fake_request)
    piwik_tracker.set_api_url(config.MATOMO_API_URL)
    if config.MATOMO_TOKEN_AUTH:
        piwik_tracker.set_token_auth(config.MATOMO_TOKEN_AUTH)
        piwik_tracker.set_ip(client_ip)
    visited_url = fake_request.META['PATH_INFO'][:1000]
    piwik_tracker.do_track_page_view(visited_url)
