import os
from dataclasses import dataclass

from eoxserver.services.ows.decoders import (
    OWSCommonKVPDecoder, OWSCommonXMLDecoder
)

from edc_ogc.ogc.wms import (
    dispatch_wms_get_map, dispatch_wms_get_capabilities,
    WMS11GetMapDecoder, WMS13GetMapDecoder
)

from edc_ogc.ogc.wcs import dispatch_wcs

@dataclass
class OGCRequest:
    base_url: str = None
    method: str = None
    body: str = None
    query: str = None
    headers: dict = None


class OGCClient:
    def __init__(self, mdi_client, config_client, instance_id):
        self.mdi_client = mdi_client
        self.config_client = config_client
        self.instance_id = instance_id

    def dispatch(self, request: OGCRequest):
        if request.method == 'GET':
            decoder = OWSCommonKVPDecoder(request.query)
        elif request.method == 'POST':
            decoder = OWSCommonXMLDecoder(request.body)

        ows_url = os.environ.get('OWS_URL')

        scheme = request.headers.get('X-Forwarded-Scheme')
        host = request.headers.get('X-Forwarded-Host')
        uri = request.headers.get('X-Original-Uri')
        if scheme and host and uri:
            ows_url = f'{scheme}://{host}{uri}'
        else:
            ows_url = request.base_url

        service = decoder.service

        if service == 'WMS':
            return self.dispatch_wms(decoder, request, ows_url)

        elif service == 'WCS':
            return self.dispatch_wcs(decoder, request, ows_url)

    def dispatch_wms(self, ows_decoder, request, ows_url):
        ows_request = ows_decoder.request
        version = ows_decoder.version

        if ows_request == 'GETCAPABILITIES':
            return dispatch_wms_get_capabilities(self.config_client, ows_url, version)
        if ows_request == 'GETMAP':
            if version == (1, 1):
                wms_request = WMS11GetMapDecoder(request.query)
            elif version == (1, 3):
                wms_request = WMS13GetMapDecoder(request.query)
            else:
                raise Exception(f'Version {version} not supported')

            return dispatch_wms_get_map(self.mdi_client, self.config_client, wms_request)
    
    def dispatch_wcs(self, ows_decoder, request, ows_url):
        return dispatch_wcs(ows_decoder, request, ows_url, self.config_client, self.mdi_client)
