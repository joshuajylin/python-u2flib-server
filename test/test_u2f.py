# Copyright (c) 2013 Yubico AB
# All rights reserved.
#
#   Redistribution and use in source and binary forms, with or
#   without modification, are permitted provided that the following
#   conditions are met:
#
#    1. Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#    2. Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from u2flib_server.u2f import (begin_registration, complete_registration,
                               begin_authentication, complete_authentication)
from u2flib_server.model import U2fRegisterRequest, U2fSignRequest
from u2flib_server.utils import websafe_decode
from .soft_u2f_v2 import SoftU2FDevice
import unittest

APP_ID = 'https://www.example.com'
APP_ID = 'http://www.example.com/appid'
FACET = 'http://www.example.com'
FACETS = [FACET]


def register_token(devices=[]):
    token = SoftU2FDevice()
    request = begin_registration(APP_ID, devices)
    data = request.data_for_client
    response = token.register(FACET, data['appId'], data['registerRequests'][0])
    device, cert = complete_registration(request.json, response)
    return device, token


class U2fTest(unittest.TestCase):

    def test_register_fixed_values(self):
        req = U2fRegisterRequest.create(
            'http://localhost:8081',
            [],
            websafe_decode('KEzvDDdHwnXtPHIMb0Uh43hgOJ-wQTsdLujGkeg6JxM')
        )
        reg, cert = req.complete({
            "version": "U2F_V2",
            "registrationData": "BQS94xQL46G4vheJPkYSuEteM6Km4-MwgBAu1zZ6MAbjDD"
            "gqhYbpHuIhhGOKjedeDd58qqktqOJsby9wMdHGnUtVQD8ISPywVi3J6SaKebCVQdHP"
            "u3_zQigRS8LhoDwKT5Ed3tg8AWuNw9XBZEh4doEDxKGuInFazirUw8acOu2qDcEwgg"
            "IjMIIBDaADAgECAgRyuHt0MAsGCSqGSIb3DQEBCzAPMQ0wCwYDVQQDEwR0ZXN0MB4X"
            "DTE1MDkwNDA3MTAyNloXDTE2MDkwMzA3MTAyNlowKjEoMCYGA1UEAxMfWXViaWNvIF"
            "UyRiBFRSBTZXJpYWwgMTkyNDY5Mjg1MjBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IA"
            "BC37i_h-xmEtGfWnuvj_BmuhtU18MKShNP_vZ7C2WJwj8OHaSLnzAfha14CMUPaKPt"
            "RFfP6w9CFGhvEizH33XZKjOzA5MCIGCSsGAQQBgsQKAgQVMS4zLjYuMS40LjEuNDE0"
            "ODIuMS4yMBMGCysGAQQBguUcAgEBBAQDAgQwMAsGCSqGSIb3DQEBCwOCAQEAab7fWl"
            "J-lOR1sqIxawPU5DWZ1b9nQ0QmNNoetPHJ_fJC95r0esRq5axfmGufbNktNWanHww7"
            "i9n5WWxSaMTWuJSF0eAXUajo8odYA8nB4_0I6z615MWa9hTU64Pl9HlqkR5ez5jndm"
            "JNuAfhaIF4h062Jw051kMo_aENxuLixnybTfJG7Q5KRE00o2MFs5b9L9fzhDtBzv5Z"
            "-vGOefuiohowpwnxIA9l0tGqrum9plUdx06K9TqKMRDQ8naosy01rbouA6i5xVjl-t"
            "HT3z-r__FYcSZ_dQ5-SCPOh4F0w6T0UwzymQmeqYN3pP-UUgnJ-ihD-uhEWklKNYRy"
            "0K0G0jBGAiEA7rbbx2jwC1YGICkZMR07ggKWaHCwFBxNDW3OwhLNNzUCIQCSq0sjGS"
            "UnWMQgPEImrmd3tMKcbrjI995rti6UYozqsg",
            "clientData": "eyJvcmlnaW4iOiAiaHR0cDovL2xvY2FsaG9zdDo4MDgxIiwgImNo"
            "YWxsZW5nZSI6ICJLRXp2RERkSHduWHRQSElNYjBVaDQzaGdPSi13UVRzZEx1akdrZW"
            "c2SnhNIiwgInR5cCI6ICJuYXZpZ2F0b3IuaWQuZmluaXNoRW5yb2xsbWVudCJ9"
        })
        assert reg

    def test_authenticate_fixed_values(self):
        device = {
            'version': 'U2F_V2',
            'publicKey': 'BBCcnAOknoMgokEGuTdfpNLQ-uylwlKp_xbEW8urjJsXKv9XZSL-V'
            '8C2nwcPEckav1mKZFr5K96uAoLtuxOUf-E',
            'keyHandle': 'BIarIKfyMqyf4bEI6tOqGInAfHrrQkMA2eyPJlNnInbAG1tXNpdRs'
            '48ef92_b1-mfN4VhaTWxo1SGoxT6CIanw',
            'appId': 'http://www.example.com/appid'
        }
        response = {
            'keyHandle': 'BIarIKfyMqyf4bEI6tOqGInAfHrrQkMA2eyPJlNnInbAG1tXNpdRs'
            '48ef92_b1-mfN4VhaTWxo1SGoxT6CIanw',
            'signatureData': 'AAAAAAEwRQIhAJrcBSpaDprFzXmVw60r6x-_gOZ0t-8v7DGii'
            'Kmar0SAAiAYKKEX41nWUCLLoKiBYuHYdPP1MPPNQ0cX_JIybPtThA',
            'clientData': 'eyJvcmlnaW4iOiAiaHR0cHM6Ly93d3cuZXhhbXBsZS5jb20iLCAi'
            'Y2hhbGxlbmdlIjogIm9JZXUtblB4eDlEY0Y3TF9EQ0Uza3ZZb3gtYzRVdXZGYjhsTk'
            'c2dGgxMG8iLCAidHlwIjogIm5hdmlnYXRvci5pZC5nZXRBc3NlcnRpb24ifQ'
        }
        req = U2fSignRequest.create(
            'http://www.example.com/appid',
            [device],
            websafe_decode('oIeu-nPxx9DcF7L_DCE3kvYox-c4UuvFb8lNG6th10o')
        )
        req.complete(response)

    def test_register_soft_u2f(self):
        device, token = register_token()
        assert device

    def test_authenticate_single_soft_u2f(self):
        # Register
        device, token = register_token()

        # Authenticate
        request = begin_authentication(APP_ID, [device])
        data = request.data_for_client

        response = token.getAssertion(
            FACET,
            data['appId'],
            data['challenge'],
            data['registeredKeys'][0]
        )

        complete_authentication(request.json, response)

    def test_authenticate_multiple_soft_u2f(self):
        # Register
        device1, token1 = register_token()
        device2, token2 = register_token([device1])

        # Authenticate
        request = begin_authentication(APP_ID, [device1, device2])
        data = request.data_for_client
        response = token1.getAssertion(
            FACET,
            data['appId'],
            data['challenge'],
            data['registeredKeys'][0]
        )

        complete_authentication(request.json, response)

    def test_authenticate_soft_u2f(self):
        device, token = register_token()

        challenge1 = U2fSignRequest.create(APP_ID, [device])
        data1 = challenge1.data_for_client
        challenge2 = U2fSignRequest.create(APP_ID, [device])
        data2 = challenge2.data_for_client

        response2 = token.getAssertion(
            FACET,
            data2['appId'],
            data2['challenge'],
            data2['registeredKeys'][0]
        )
        response1 = token.getAssertion(
            FACET,
            data1['appId'],
            data1['challenge'],
            data1['registeredKeys'][0]
        )

        challenge1.complete(response1)
        challenge2.complete(response2)

        try:
            challenge1.complete(response2)
        except:
            pass
        else:
            assert False, "Incorrect validation should fail!"

        try:
            challenge2.complete(response1)
        except:
            pass
        else:
            assert False, "Incorrect validation should fail!"

    def test_wrong_facet(self):
        token = SoftU2FDevice()
        request = U2fRegisterRequest.create(APP_ID, [])
        data = request.data_for_client
        response = token.register(
            "http://wrongfacet.com",
            data['appId'],
            data['registerRequests'][0]
        )

        try:
            request.complete(response, FACETS)
        except:
            pass
        else:
            assert False, "Incorrect facet should fail!"

        response2 = token.register(
            FACET,
            data['appId'],
            data['registerRequests'][0]
        )
        device, cert = request.complete(response2, FACETS)

        signreq = U2fSignRequest.create(APP_ID, [device])
        data = signreq.data_for_client
        response = token.getAssertion(
            'http://notright.com',
            data['appId'],
            data['challenge'],
            data['registeredKeys'][0]
        )

        try:
            signreq.complete(response, FACETS)
        except:
            pass
        else:
            assert False, "Incorrect facet should fail!"
