import os
import unittest
import logging

import oauthlib.oauth2
import requests_oauthlib

from edc_ogc.mdi import Mdi

HAS_SH_CREDENTIALS = 'SH_CLIENT_ID' in os.environ and 'SH_CLIENT_SECRET' in os.environ
REQUIRE_SH_CREDENTIALS = 'requires SH credentials'


logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)

TEST_EVALSCRIPT = """//VERSION=3
function setup() {
  return {
    input: ["B02", "B03", "B04"],
    output: { bands: 3 }
  };
}

function evaluatePixel(sample) {
  return [2.5 * sample.B04, 2.5 * sample.B03, 2.5 * sample.B02];
}
"""


class ConfigClientMock:
    def get_evalscript_and_defaults(self, *args):
        return TEST_EVALSCRIPT, {
            "type": "S2L1C",
            "mosaickingOrder": "mostRecent",
            "maxCloudCoverage": 50,
            "temporal": False,
        }


class MdiTest(unittest.TestCase):

    @staticmethod
    def get_mdi() -> Mdi:
        client_id = os.environ.get('SH_CLIENT_ID')
        client_secret = os.environ.get('SH_CLIENT_SECRET')
        # instance_id = os.environ.get("SH_INSTANCE_ID")

        client = oauthlib.oauth2.BackendApplicationClient(client_id=client_id)
        session = requests_oauthlib.OAuth2Session(client=client)

        mdi = Mdi(
            client_id=client_id,
            client_secret=client_secret
        )
        return mdi

    # @unittest.skipUnless(HAS_SH_CREDENTIALS, REQUIRE_SH_CREDENTIALS)
    # def test_image(self):
    #     mdi = self.get_mdi()
    #     output = mdi.process_image(
    #         sources=['S2L1C'],
    #         bbox=(14.043549, 46.580095, 14.167831, 46.652688),
    #         # crs='http://www.opengis.net/def/crs/OGC/1.3/CRS84',
    #         crs='EPSG:4326',
    #         width=512,
    #         height=512,
    #         format='image/png',
    #         evalscript=TEST_EVALSCRIPT,
    #     )
    #     with open('out.png', 'wb') as f:
    #         f.write(output)


    # def test_dispatch_get_map(self):
    #     class ConfigClientMock:
    #         def get_evalscript_and_defaults(self, *args):
    #             return TEST_EVALSCRIPT, {
    #                 "type": "S2L1C",
    #                 "mosaickingOrder": "mostRecent",
    #                 "maxCloudCoverage": 50,
    #                 "temporal": False,
    #             }

    #     class WMSRequest:
    #         version = (1, 3, 0)
    #         layers = ['TRUE_COLOR']
    #         styles = ['default']
    #         crs = 'EPSG:4326'
    #         bbox = (46.580095, 14.043549, 46.652688, 14.167831)
    #         width = 512
    #         height = 512
    #         format = 'image/png'
    #         time = None

    #     mdi = self.get_mdi()
    #     config_client = ConfigClientMock()
    #     wms_request = WMSRequest()

    #     with open('out.png', 'wb') as f:
    #         f.write(
    #             dispatch_wms_get_map(mdi, config_client, wms_request)
    #         )

    def test_capabilities(self):
        # from edc_ogc.ogc.wms import dispatch_wms_get_capabilities
        #dispatch_wms_get_capabilities(None, None)
        pass

    def test_parse_request(self):
        from edc_ogc.configapi import ConfigAPIDefaultLayers
        from edc_ogc.ogc.client import OGCClient, OGCRequest
        from edc_ogc.ogc.wms import WMS11GetMapDecoder, WMS13GetMapDecoder

        decoders = [
            WMS11GetMapDecoder('service=WMS&version=1.1.0&request=GetMap&layers=a&styles=b&srs=EPSG:4326&bbox=-180,-90,180,90&width=512&height=256&format=image/png'),
            WMS13GetMapDecoder('service=WMS&version=1.3.0&request=GetMap&layers=a&styles=b&crs=EPSG:4326&bbox=-90,-180,90,180&width=512&height=256&format=image/png'),
        ]

        for decoder in decoders:
            assert decoder.bbox
            self.assertEqual('EPSG:4326', decoder.crs)

        client_id = os.environ.get('SH_CLIENT_ID')
        client_secret = os.environ.get('SH_CLIENT_SECRET')
        client = OGCClient(ConfigAPIDefaultLayers(client_id, client_secret), 'None')

        # response, _ = client.dispatch(OGCRequest(
        #     method='GET',
        #     query='service=WMS&version=1.3.0&request=GetMap&layers=TRUE_COLOR&styles=&crs=EPSG:4326&bbox=46.580095,14.043549,46.652688,14.167831&width=512&height=512&format=image/png',
        # ))

        response, _ = client.dispatch(OGCRequest(
            method='GET',
            query='SERVICE=WMS&VERSION=1.3.0&REQUEST=GetMap&FORMAT=image%2Fpng&TRANSPARENT=true&LAYERS=SWE&time=2021-01-22T21%3A13%3A46%2F2021-01-26T10%3A40%3A40&WIDTH=512&HEIGHT=512&CRS=EPSG%3A4326&BBOX=46.1,11.7,46.3,11.8',
            base_url='http://testserver.org/',
        ))

        with open('out.png', 'wb') as f:
            f.write(response)

        response, _ = client.dispatch(OGCRequest(
            method='GET',
            query='service=WMS&version=1.1.0&request=GetCapabilities',
            base_url='http://testserver.org/',
        ))

        with open('out.xml', 'wb') as f:
            f.write(response)

    # @unittest.skipUnless(HAS_SH_CREDENTIALS, REQUIRE_SH_CREDENTIALS)
    # def test_woerthersee(self):
    #     request = Mdi.prepare_request(
    #         'S2L2A',
    #         ['B04', 'B03', 'B02'],
    #         ['t0', 't1', 't2', 't3'],
    #         (512, 512),
    #         ("2019-06-10T00:00:00Z", "2019-06-20T00:00:00Z"),
    #         (14.043549,46.580095,14.167831,46.652688)
    #     )

    #     with open(os.path.join(os.path.dirname(__file__), 'request_woerthersee.json'), 'w') as fp:
    #         json.dump(request, fp, indent=2)

    #     mdi = Mdi()

    #     t1 = time.perf_counter()
    #     mime_type, data = mdi.post_request(request)
    #     t2 = time.perf_counter()
    #     print(f"test_single_band: took {t2 - t1} secs")

    #     self.assertEqual('application/tar', mime_type)

    #     with open(os.path.join(os.path.dirname(__file__), 'response_woerthersee.tar'), 'wb') as fp:
    #         fp.write(data)

    #     mdi.close()


# class ConfigAPITest(unittest.TestCase):

#     def test_layers(self):
#         client_id = os.environ.get('SH_CLIENT_ID')
#         client_secret = os.environ.get('SH_CLIENT_SECRET')
#         instance_id = os.environ["SH_INSTANCE_ID"]

#         print('client_id', client_id)
#         print('client_secret', client_secret)
#         print('instance_id', instance_id)

#         # )
#         # client = oauthlib.oauth2.BackendApplicationClient(client_id=client_id)
#         # session = requests_oauthlib.OAuth2Session(client=client)
#         # token = session.fetch_token(
#         #     token_url='https://services.sentinel-hub.com/oauth' + '/token',
#         #     client_id=client_id,
#         #     client_secret=client_secret
#         # )


#         client_id = client_id or os.environ.get('SH_CLIENT_ID')
#         client_secret = client_secret or os.environ.get('SH_CLIENT_SECRET')

#         client = oauthlib.oauth2.BackendApplicationClient(client_id=client_id)
#         session = requests_oauthlib.OAuth2Session(client=client)

#         oauth2_url= 'https://services.sentinel-hub.com/oauth'
#         token = session.fetch_token(token_url=oauth2_url + '/token',
#                                                 client_id=client_id,
#                                                 client_secret=client_secret)



#         print(token)
#         api = ConfigAPI(session, instance_id)
#         api.get_layers()
