import os
import logging
import logging.config


from flask import Flask, request, Response, jsonify, send_from_directory
import oauthlib.oauth2
import requests_oauthlib

from edc_ogc import VERSION
from edc_ogc.ogc.client import OGCClient, OGCRequest
from edc_ogc.configapi import ConfigAPIMock, ConfigAPI
from edc_ogc.mdi import Mdi, MdiError
from prometheus_flask_exporter import PrometheusMetrics

# -------------- App setup --------------
app = Flask(__name__, static_url_path='/static')

metrics = PrometheusMetrics(app)

metrics.info('app_info', 'Application info', version=VERSION)


# -------------- Logging setup --------------

logger = logging.getLogger(__name__)

logging.config.dictConfig({
    'version': 1,
    'formatters': {
        'simple': {
            'format': '%(levelname)s: %(message)s',
        },
        'verbose': {
            'format': '[%(asctime)s][%(module)s] %(levelname)s: %(message)s',
        }
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            # 'filters': ['require_debug_true'],
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'edc_ogc': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'requests': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'oauthlib': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'requests_oauthlib': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
})

# -------------- Utilities --------------

def create_session():
    client_id = os.environ.get('SH_CLIENT_ID')
    client_secret = os.environ.get('SH_CLIENT_SECRET')

    client = oauthlib.oauth2.BackendApplicationClient(client_id=client_id)
    session = requests_oauthlib.OAuth2Session(client=client)
    return session, client_id, client_secret

def get_mdi() -> Mdi:
    client_id = os.environ.get('SH_CLIENT_ID')
    client_secret = os.environ.get('SH_CLIENT_SECRET')

    client = oauthlib.oauth2.BackendApplicationClient(client_id=client_id)
    session = requests_oauthlib.OAuth2Session(client=client)

    mdi = Mdi(
        session=session,
        client_id=client_id,
        client_secret=client_secret
    )
    return mdi

CLIENTS = {}

def get_client(instance_id=None):
    if instance_id not in CLIENTS:
        datasets_path = os.environ.get('DATASETS_PATH')
        layers_path = os.environ.get('LAYERS_PATH')
        dataproducts_path = os.environ.get('DATAPRODUCTS_PATH')
        client_id = os.environ.get('SH_CLIENT_ID')
        client_secret = os.environ.get('SH_CLIENT_SECRET')

        if instance_id is None:
            config_api = ConfigAPIMock(
                datasets_path=datasets_path,
                layers_path=layers_path,
                dataproducts_path=dataproducts_path
            )
        else:
            config_api = ConfigAPI(
                client_id, client_secret, instance_id
            )

        CLIENTS[instance_id] = OGCClient(
            get_mdi(),
            config_api,
            'None'
        )

    return CLIENTS[instance_id]


# -------------- Routes --------------

@app.route('/version')
def version():
    return Response(response=f"{VERSION}")


@app.route('/headers')
def headers():
    return jsonify(dict(request.headers))


@app.route('/')
def ows():
    if not request.query_string.decode('ascii'):
        return app.send_static_file('index.html')
    try:
        client = get_client()
        ogc_request = OGCRequest(
            base_url=request.base_url,
            method=request.method,
            query=request.query_string.decode('ascii'),
            headers=request.headers,
        )
        result = client.dispatch(ogc_request)
        if len(result) == 2:
            response, mimetype = result
            status = 200
        elif len(result) == 3:
            response, mimetype, status = result

        return Response(response=response, mimetype=mimetype, status=status, headers={
            'Access-Control-Allow-Origin': '*'
        })
    except Exception as e:
        logger.exception(e)
        return Response(response=f'an error occured: {e}', status=400)


@app.route('/<instance_id>')
def ows_instance(instance_id):
    if not request.query_string.decode('ascii'):
        return app.send_static_file('index.html')
    try:
        client = get_client(instance_id)
        ogc_request = OGCRequest(
            base_url=request.base_url,
            method=request.method,
            query=request.query_string.decode('ascii'),
            headers=request.headers,
        )
        result = client.dispatch(ogc_request)
        if len(result) == 2:
            response, mimetype = result
            status = 200
        elif len(result) == 3:
            response, mimetype, status = result

        return Response(response=response, mimetype=mimetype, status=status, headers={
            'Access-Control-Allow-Origin': '*'
        })
    except Exception as e:
        logger.exception(e)
        return Response(response=f'an error occured: {e}', status=400)
