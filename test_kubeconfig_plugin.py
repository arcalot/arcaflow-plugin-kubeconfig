#!/usr/bin/env python3
import unittest
import yaml

from arcaflow_plugin_sdk import plugin

import kubeconfig_plugin


class KubeconfigPluginTest(unittest.TestCase):
    @staticmethod
    def test_serialization():
        plugin.test_object_serialization(
            kubeconfig_plugin.InputParams("kubeconfig: apiVersion: v1clusters:")
        )

        plugin.test_object_serialization(
            kubeconfig_plugin.kubeconfig_output_schema.unserialize(
                {
                    "connection": {
                        "host": ("https://api.nonexistent.arcalot.io:6443"),
                        "cacert": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUI0VENDQVl1Z0F3SUJBZ0lVQ0hoaGZmWTFsemV6R2F0WU1SMDJncEVKQ2hrd0RRWUpLb1pJaHZjTkFRRUwKQlFBd1JURUxNQWtHQTFVRUJoTUNRVlV4RXpBUkJnTlZCQWdNQ2xOdmJXVXRVM1JoZEdVeElUQWZCZ05WQkFvTQpHRWx1ZEdWeWJtVjBJRmRwWkdkcGRITWdVSFI1SUV4MFpEQWVGdzB5TWpBNU1qZ3dOVEk0TVRKYUZ3MHlNekE1Ck1qZ3dOVEk0TVRKYU1FVXhDekFKQmdOVkJBWVRBa0ZWTVJNd0VRWURWUVFJREFwVGIyMWxMVk4wWVhSbE1TRXcKSHdZRFZRUUtEQmhKYm5SbGNtNWxkQ0JYYVdSbmFYUnpJRkIwZVNCTWRHUXdYREFOQmdrcWhraUc5dzBCQVFFRgpBQU5MQURCSUFrRUFycjg5ZjJrZ2dTTy95YUNCNkV3SVFlVDZacHRCb1gwWnZDTUkrRHBrQ3dxT1M1ZndSYmoxCm5FaVBuTGJ6RERnTVU4S0NQQU1oSTdKcFlSbEhuaXB4V3dJREFRQUJvMU13VVRBZEJnTlZIUTRFRmdRVWlaNkoKRHd1RjlRQ2gxdndRR1hzMk11dHVROUV3SHdZRFZSMGpCQmd3Rm9BVWlaNkpEd3VGOVFDaDF2d1FHWHMyTXV0dQpROUV3RHdZRFZSMFRBUUgvQkFVd0F3RUIvekFOQmdrcWhraUc5dzBCQVFzRkFBTkJBRllJRk0yN0JEaUc3MjVkClZraFJibGt2WnplUkhoY3d0RE9RVEM5ZDhNL0x5bU4yeTBuSFNsSkNabS9Mby9hSDh2aVNZMXZpMUdTSGZEejcKVGxmZThncz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",  # noqa: E501
                        "cert": "LS0tLS1CRUdJTiBDRVJUSUZJQ0FURS0tLS0tCk1JSUI0VENDQVl1Z0F3SUJBZ0lVQ0hoaGZmWTFsemV6R2F0WU1SMDJncEVKQ2hrd0RRWUpLb1pJaHZjTkFRRUwKQlFBd1JURUxNQWtHQTFVRUJoTUNRVlV4RXpBUkJnTlZCQWdNQ2xOdmJXVXRVM1JoZEdVeElUQWZCZ05WQkFvTQpHRWx1ZEdWeWJtVjBJRmRwWkdkcGRITWdVSFI1SUV4MFpEQWVGdzB5TWpBNU1qZ3dOVEk0TVRKYUZ3MHlNekE1Ck1qZ3dOVEk0TVRKYU1FVXhDekFKQmdOVkJBWVRBa0ZWTVJNd0VRWURWUVFJREFwVGIyMWxMVk4wWVhSbE1TRXcKSHdZRFZRUUtEQmhKYm5SbGNtNWxkQ0JYYVdSbmFYUnpJRkIwZVNCTWRHUXdYREFOQmdrcWhraUc5dzBCQVFFRgpBQU5MQURCSUFrRUFycjg5ZjJrZ2dTTy95YUNCNkV3SVFlVDZacHRCb1gwWnZDTUkrRHBrQ3dxT1M1ZndSYmoxCm5FaVBuTGJ6RERnTVU4S0NQQU1oSTdKcFlSbEhuaXB4V3dJREFRQUJvMU13VVRBZEJnTlZIUTRFRmdRVWlaNkoKRHd1RjlRQ2gxdndRR1hzMk11dHVROUV3SHdZRFZSMGpCQmd3Rm9BVWlaNkpEd3VGOVFDaDF2d1FHWHMyTXV0dQpROUV3RHdZRFZSMFRBUUgvQkFVd0F3RUIvekFOQmdrcWhraUc5dzBCQVFzRkFBTkJBRllJRk0yN0JEaUc3MjVkClZraFJibGt2WnplUkhoY3d0RE9RVEM5ZDhNL0x5bU4yeTBuSFNsSkNabS9Mby9hSDh2aVNZMXZpMUdTSGZEejcKVGxmZThncz0KLS0tLS1FTkQgQ0VSVElGSUNBVEUtLS0tLQo=",  # noqa: E501
                        "key": "LS0tLS1CRUdJTiBQUklWQVRFIEtFWS0tLS0tCk1JSUJWQUlCQURBTkJna3Foa2lHOXcwQkFRRUZBQVNDQVQ0d2dnRTZBZ0VBQWtFQXJyODlmMmtnZ1NPL3lhQ0IKNkV3SVFlVDZacHRCb1gwWnZDTUkrRHBrQ3dxT1M1ZndSYmoxbkVpUG5MYnpERGdNVThLQ1BBTWhJN0pwWVJsSApuaXB4V3dJREFRQUJBa0J5YnUveDBNRWxjR2kydS9KMlVkd1Njc1Y3amU1VHQxMno4Mmw3VEptWkZGSjhSTG1jCnJoMDBHdmViNFZwR2hkMStjM2xaYk8xbUlUNnYzdkhNOUEwaEFpRUExNEVXNmIrOTlYWXphNys1dXdJRHVpTSsKQnozcGtLKzl0bGZWWEU3SnlLc0NJUURQbFlKNXh0YnVUK1Z2QjNYT2REL1ZXaUVxRW12RTNmbFYwNDE3UnFoYQpFUUlnYnl4d05wd3RFZ0V0Vzh1bnRCckE4M2lVMmtXTlJZL3o3YXA0TGt1Uyswc0NJR2UyRSswUm1mcVFzbGxwCmljTXZNMkU5MllueWtDTlluNlR3d0NRU0pqUnhBaUVBbzlNbWFWbEs3WWRoU01QbzUydUpZemQ5TVFaSnFocSsKbEIxWkdEeC9BUkU9Ci0tLS0tRU5EIFBSSVZBVEUgS0VZLS0tLS0K",  # noqa: E501
                    },
                }
            )
        )

        plugin.test_object_serialization(
            kubeconfig_plugin.ErrorOutput(error="This is an error")
        )

    EXPECTED_TOKEN = '''-----BEGIN CERTIFICATE-----
MIIB4TCCAYugAwIBAgIUCHhhffY1lzezGatYMR02gpEJChkwDQYJKoZIhvcNAQEL
BQAwRTELMAkGA1UEBhMCQVUxEzARBgNVBAgMClNvbWUtU3RhdGUxITAfBgNVBAoM
GEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDAeFw0yMjA5MjgwNTI4MTJaFw0yMzA5
MjgwNTI4MTJaMEUxCzAJBgNVBAYTAkFVMRMwEQYDVQQIDApTb21lLVN0YXRlMSEw
HwYDVQQKDBhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQwXDANBgkqhkiG9w0BAQEF
AANLADBIAkEArr89f2kggSO/yaCB6EwIQeT6ZptBoX0ZvCMI+DpkCwqOS5fwRbj1
nEiPnLbzDDgMU8KCPAMhI7JpYRlHnipxWwIDAQABo1MwUTAdBgNVHQ4EFgQUiZ6J
DwuF9QCh1vwQGXs2MutuQ9EwHwYDVR0jBBgwFoAUiZ6JDwuF9QCh1vwQGXs2Mutu
Q9EwDwYDVR0TAQH/BAUwAwEB/zANBgkqhkiG9w0BAQsFAANBAFYIFM27BDiG725d
VkhRblkvZzeRHhcwtDOQTC9d8M/LymN2y0nHSlJCZm/Lo/aH8viSY1vi1GSHfDz7
Tlfe8gs=
-----END CERTIFICATE-----
'''
    EXPECTED_KEY = '''-----BEGIN PRIVATE KEY-----
MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEArr89f2kggSO/yaCB
6EwIQeT6ZptBoX0ZvCMI+DpkCwqOS5fwRbj1nEiPnLbzDDgMU8KCPAMhI7JpYRlH
nipxWwIDAQABAkBybu/x0MElcGi2u/J2UdwScsV7je5Tt12z82l7TJmZFFJ8RLmc
rh00Gveb4VpGhd1+c3lZbO1mIT6v3vHM9A0hAiEA14EW6b+99XYza7+5uwIDuiM+
Bz3pkK+9tlfVXE7JyKsCIQDPlYJ5xtbuT+VvB3XOdD/VWiEqEmvE3flV0417Rqha
EQIgbyxwNpwtEgEtW8untBrA83iU2kWNRY/z7ap4LkuS+0sCIGe2E+0RmfqQsllp
icMvM2E92YnykCNYn6TwwCQSJjRxAiEAo9MmaVlK7YdhSMPo52uJYzd9MQZJqhq+
lB1ZGDx/ARE=
-----END PRIVATE KEY-----
'''


    def test_functional_token(self):
        with open("tests/test_token.yaml", "r") as f:
            test_input = f.read()
        parsed_input = yaml.safe_load(test_input)
        input = kubeconfig_plugin.InputParams(kubeconfig=parsed_input["kubeconfig"])
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("success", result)
        plugin.test_object_serialization(data)
        conn = data.connection
        self.assertEqual("sha256~2Z70unz91xNLI43k7MnM_mTbIfwe1EVHuxEXDiFWM9c", conn.bearerToken)
        self.assertEqual(self.EXPECTED_TOKEN, conn.cacert)
        self.assertEqual(None, conn.cert)
        self.assertEqual(None, conn.key)
        self.assertEqual(None, conn.username)
        self.assertEqual(None, conn.password)

    def test_functional_client_cert(self):
        with open("tests/test_client_cert.yaml", "r") as f:
            test_input = f.read()
        parsed_input = yaml.safe_load(test_input)
        input = kubeconfig_plugin.InputParams(kubeconfig=parsed_input["kubeconfig"])
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("success", result)
        plugin.test_object_serialization(data)
        conn = data.connection
        self.assertEqual(None, conn.bearerToken)
        self.assertEqual(conn.cert, self.EXPECTED_TOKEN)
        self.assertEqual(conn.key, self.EXPECTED_KEY)
        self.assertEqual(None, conn.username)
        self.assertEqual(None, conn.password)

    def test_functional_username(self):
        with open("tests/test_username.yaml", "r") as f:
            test_input = f.read()
        parsed_input = yaml.safe_load(test_input)
        input = kubeconfig_plugin.InputParams(kubeconfig=parsed_input["kubeconfig"])
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("success", result)
        plugin.test_object_serialization(data)
        conn = data.connection
        self.assertEqual(None, conn.bearerToken)
        self.assertEqual(None, conn.cert)
        self.assertEqual(None, conn.key)
        self.assertEqual("admin", conn.username)
        self.assertEqual("test", conn.password)


if __name__ == "__main__":
    unittest.main()
