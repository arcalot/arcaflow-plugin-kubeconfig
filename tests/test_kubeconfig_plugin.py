#!/usr/bin/env python3

import unittest
import yaml
import sys
from arcaflow_plugin_sdk import plugin
# import kubeconfig_plugin
from arcaflow_plugin_kubeconfig import kubeconfig_plugin


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

    EXPECTED_TOKEN = """-----BEGIN CERTIFICATE-----
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
"""
    EXPECTED_KEY = """-----BEGIN PRIVATE KEY-----
MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEArr89f2kggSO/yaCB
6EwIQeT6ZptBoX0ZvCMI+DpkCwqOS5fwRbj1nEiPnLbzDDgMU8KCPAMhI7JpYRlH
nipxWwIDAQABAkBybu/x0MElcGi2u/J2UdwScsV7je5Tt12z82l7TJmZFFJ8RLmc
rh00Gveb4VpGhd1+c3lZbO1mIT6v3vHM9A0hAiEA14EW6b+99XYza7+5uwIDuiM+
Bz3pkK+9tlfVXE7JyKsCIQDPlYJ5xtbuT+VvB3XOdD/VWiEqEmvE3flV0417Rqha
EQIgbyxwNpwtEgEtW8untBrA83iU2kWNRY/z7ap4LkuS+0sCIGe2E+0RmfqQsllp
icMvM2E92YnykCNYn6TwwCQSJjRxAiEAo9MmaVlK7YdhSMPo52uJYzd9MQZJqhq+
lB1ZGDx/ARE=
-----END PRIVATE KEY-----
"""

    def get_kubeconfig_test_value(self, filename):
        with open(filename, "r") as f:
            test_input = f.read()
        parsed_input = yaml.safe_load(test_input)
        return parsed_input["kubeconfig"]

    def test_functional_token(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_token.yaml")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        # This is the happy case, so if it fails, print the error data
        if result != "success":
            print(f"Functional test failed. Error data: {data.error}", file=sys.stderr)
        self.assertEqual("success", result)
        plugin.test_object_serialization(data)
        conn = data.connection
        self.assertEqual(
            "sha256~2Z70unz91xNLI43k7MnM_mTbIfwe1EVHuxEXDiFWM9c", conn.bearerToken
        )
        self.assertEqual(self.EXPECTED_TOKEN, conn.cacert)
        self.assertEqual(None, conn.cert)
        self.assertEqual(None, conn.key)
        self.assertEqual(None, conn.username)
        self.assertEqual(None, conn.password)

    def test_functional_client_cert(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_client_cert.yaml")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
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
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("success", result)
        plugin.test_object_serialization(data)
        conn = data.connection
        self.assertEqual(None, conn.bearerToken)
        self.assertEqual(None, conn.cert)
        self.assertEqual(None, conn.key)
        self.assertEqual("admin", conn.username)
        self.assertEqual("test", conn.password)

    def test_invalid_yaml(self):
        input = kubeconfig_plugin.InputParams(kubeconfig="\tyaml-can't-have-tabs")
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("not valid YAML", data.error)

    def test_missing_kind(self):
        # Empty file
        input = kubeconfig_plugin.InputParams(kubeconfig="{}")
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("missing 'kind' field", data.error)

        # Test entirely wrong yaml, but not empty.
        input = kubeconfig_plugin.InputParams(kubeconfig='a:\n    b: "Config"')
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("missing 'kind' field", data.error)

    def test_wrong_kind(self):
        # Test entirely wrong yaml, but not empty.
        input = kubeconfig_plugin.InputParams(kubeconfig="kind: NotConfig")
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("not a kubeconfig file", data.error)

    def test_missing_current_context(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        # Change current-context line
        kubeconfig = kubeconfig.replace("current-context:", "not-current-context:")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("current-context", data.error)

    def test_missing_contexts(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        # Change contexts line
        kubeconfig = kubeconfig.replace("contexts:", "not-contexts:")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("contexts", data.error)

    def test_missing_context_cluster_with_name(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        # Replacing the name that is in the context section
        kubeconfig = kubeconfig.replace("name: arcaflow-", "wrong: arcaflow-")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("'name' section missing from context", data.error)

    def test_current_context_not_in_contexts(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        # Change current-context line
        kubeconfig = kubeconfig.replace(
            "current-context: admin", "current-context: wrong"
        )
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("Failed to find", data.error)

    def test_values_in_context(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        # Remove the two needed values
        kubeconfig_no_cluster_val = kubeconfig.replace("user: admin", "wrong: wrong")
        kubeconfig_no_user_val = kubeconfig.replace("cluster: arcaflow", "wrong: wrong")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig_no_cluster_val)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("field missing", data.error)
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig_no_user_val)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("field missing", data.error)

    def test_missing_clusters(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        kubeconfig = kubeconfig.replace("clusters:", "notclusters:")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("Clusters section missing", data.error)

    def test_missing_cluster_section(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        kubeconfig = kubeconfig.replace("- cluster:", "- notcluster:")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("cluster section missing", data.error)

    def test_missing_clusters_cluster_with_name(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        # Replacing the name section in the clusters -> cluster position
        kubeconfig = kubeconfig.replace("name: arcaflow\n", "name: wrong\n")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("Failed to find a cluster", data.error)

    def test_missing_cluster_name_section(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        kubeconfig = kubeconfig.replace("name: arcaflow\n", "wrong: arcaflow\n")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("'name' section missing", data.error)

    def test_missing_users(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        kubeconfig = kubeconfig.replace("users:", "wrong:")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("'users' section not found", data.error)

    def test_missing_users_section_keys(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        kubeconfig = kubeconfig.replace("- name: admin", "- wrong: admin")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("'name' section in the users", data.error)

    def test_missing_users_user_section(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        kubeconfig = kubeconfig.replace("user:\n", "wrong:\n")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("'user' section in the users", data.error)

    def test_user_not_found(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        kubeconfig = kubeconfig.replace("- name: admin", "- name: wrong")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("Failed to find a user named", data.error)

    def test_missing_server_section(self):
        kubeconfig = self.get_kubeconfig_test_value("tests/test_username.yaml")
        # Change current-context line
        kubeconfig = kubeconfig.replace("server:", "wrong:")
        input = kubeconfig_plugin.InputParams(kubeconfig=kubeconfig)
        result, data = kubeconfig_plugin.extract_kubeconfig(input)
        self.assertEqual("error", result)
        self.assertIn("Failed to find server", data.error)


if __name__ == "__main__":
    unittest.main()
