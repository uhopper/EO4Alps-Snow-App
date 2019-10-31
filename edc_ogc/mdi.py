import json
import os
import logging
from typing import List, Any, Dict, Tuple, Union, Sequence
from time import time

import oauthlib.oauth2
import requests_oauthlib
import requests
from eoxserver.core.util.timetools import isoformat


DEFAULT_OAUTH2_URL = 'https://services.sentinel-hub.com/oauth'
DEFAULT_API_URL = 'https://services.sentinel-hub.com/api/v1'


logger = logging.getLogger(__name__)


class Mdi:
    def __init__(self, client_id, client_secret, session=None,
                 api_url=DEFAULT_API_URL,
                 oauth2_url=DEFAULT_OAUTH2_URL):
        self.api_url = api_url
        self.oauth2_url = oauth2_url
        self.client_id = client_id or os.environ.get('SH_CLIENT_ID')
        self.client_secret = client_secret or os.environ.get('SH_CLIENT_SECRET')
        self.token = None

        if session is None:
            client = oauthlib.oauth2.BackendApplicationClient(client_id=client_id)
            self.session = requests_oauthlib.OAuth2Session(client=client)
        else:
            self.session = session

    def close(self):
        self.session.close()

    @property
    def token_info(self) -> Dict[str, Any]:
        resp = self.session.get(self.oauth2_url + '/tokeninfo')
        return json.loads(resp.content)

    def refresh_token(self):
        token_url = self.oauth2_url + '/token'
        logger.info(f'Fetching new access token from {token_url}')
        self.token = self.session.fetch_token(
            token_url=token_url,
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        return self.token

    def send_process_request(self, request: Dict, accept_header: str, api_url=None) -> Tuple[str, Any]:
        if not self.token:
            self.refresh_token()

        retried = False
        while True:
            try:
                logger.debug(f'Sending process request {json.dumps(request)}')
                start = time()
                resp = self.session.post(
                    (api_url or self.api_url) + '/process',
                    json=request,
                    headers={
                        'Accept': accept_header,
                        'cache-control': 'no-cache'
                    }
                )
                logger.info(f'Process request took {time() - start} seconds to complete')
                break
            except oauthlib.oauth2.TokenExpiredError:
                if retried:
                    raise

                logger.info('Token expired')
                self.refresh_token()
                retried = True

        if not resp.ok:
            reason = resp.reason
            status_code = resp.status_code
            content = resp.content
            code = None
            message = None
            try:
                values = json.loads(resp.content)['error']
                message = values['message']
                code = values['code']
            except:
                pass

            raise MdiError(
                reason,
                status_code=status_code,
                message=message,
                content=content,
                code=code,
            )

        return resp.content

    def create_data_input(self, datasource, time, upsample, downsample):
        data_filter = {}
        if time:
            from_, to = time
            data_filter['timeRange'] = {
                'from': isoformat(from_),
                'to': isoformat(to),
            }

        if 'mosaickingOrder' in datasource:
            data_filter['mosaickingOrder'] = datasource['mosaickingOrder']

        if 'collectionId' in datasource:
            data_filter['collectionId'] = datasource['collectionId']

        return {
            'type': datasource['type'],
            'dataFilter': data_filter,
            'processing': {
                'upsampling': upsample or datasource.get('upsampling', 'BILINEAR'),
                'downsampling': downsample or datasource.get('downsampling', 'BILINEAR'),
            }
        }

    def process_image(self, sources, bbox, crs, width, height, format, evalscript,
                      time=None, upsample=None, downsample=None, api_url=None):
        request_body = {
            'input': {
                'bounds': {
                    'bbox': bbox,
                    'properties': {
                        'crs': crs,
                    },
                },
                'data': [
                    self.create_data_input(source, time, upsample, downsample)
                    for source in sources
                ]
            },
            'output': {
                'width': width,
                'height': height,
                'responses': [{
                    'identifier': 'default',
                    'format': {
                        'type': format
                    }
                }]
            },
            'evalscript': evalscript,
        }
        return self.send_process_request(request_body, format, api_url)


class MdiError(Exception):
    def __init__(self, reason, status_code, message, content=None, code=None):
        super().__init__(reason)
        self.reason = reason
        self.status_code = status_code
        self.message = message
        self.content = content
        self.code = code

    def __repr__(self) -> str:
        return f'MdiError({self.reason}, {self.status_code}, details={self.content!r})'

    def __str__(self) -> str:
        text = f'{self.reason}, status code {self.status_code}'
        if self.content:
            text += f':\n{self.content}\n'
        return text