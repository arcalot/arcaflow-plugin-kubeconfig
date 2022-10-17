#!/usr/bin/env python3

import sys
import typing
from dataclasses import dataclass, field
from arcaflow_plugin_sdk import plugin, validation
from kubernetes import config
import yaml


@dataclass
class InputParams:
    """
    This is the input data structure for the kubeconfig plugin.
    """

    kubeconfig: typing.Annotated[str, validation.min(1)] = field(
        metadata={
            "name": "kubeconfig",
            "description": "input kubeconfig string",
        }
    )


@dataclass
class SuccessOutput:
    """
    This is the output data structure for the success case.
    """

    cluster_name: str = field(
        metadata={
            "name": "Cluster Name",
            "description": "Name of cluster",
        }
    )

    server_url: str = field(
        metadata={
            "name": "Server",
            "description": "Kubernetes server endpoint url",
        }
    )

    certificate_authority_data: str = field(
        metadata={
            "name": "certificate authority data",
            "description": "Cluster certificate authority",
        }
    )

    user: str = field(
        metadata={
            "name": "User",
            "description": "name of the user/service account.",
        }
    )

    client_certificate_data: typing.Optional[str] = field(
        default=None,
        metadata={
            "name": "client certificate",
            "description": "base64 encoded client cert data",
        },
    )

    client_key_data: typing.Optional[str] = field(
        default=None,
        metadata={
            "name": "client key",
            "description": "base64 encoded client key",
        },
    )

    token: typing.Optional[str] = field(
        default=None,
        metadata={
            "name": "Token",
            "description": "Secret token of the user/service account",
        },
    )


@dataclass
class ErrorOutput:
    """
    This is the output data structure in the error case.
    """

    exit_code: int = field(
        metadata={
            "name": "Exit Code",
            "description": (
                "Exit code returned by the program in case of a failure"
            ),
        }
    )
    error: str = field(
        metadata={
            "name": "Failure Error",
            "description": "Reason for failure",
        }
    )


kubeconfig_input_schema = plugin.build_object_schema(InputParams)
kubeconfig_output_schema = plugin.build_object_schema(SuccessOutput)


@plugin.step(
    id="kubeconfig",
    name="kubeconfig plugin",
    description=(
        "Inputs a kubeconfig, parses it and extracts the kubernetes cluster"
        " details "
    ),
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def extract_kubeconfig(
    params: InputParams,
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:

    print("==>> Parsing and extracting kubernetes cluster details ...")

    try:
        kubeconfig = yaml.safe_load(params.kubeconfig)
        kcl = config.kube_config.KubeConfigLoader(kubeconfig)

        output = {}
        output["cluster_name"] = kcl._current_context["context"]["cluster"]
        output["server_url"] = kcl._cluster.value["server"]
        output["certificate_authority_data"] = kcl._cluster.value[
            "certificate-authority-data"
        ]
        output["user"] = kcl._current_context["context"]["user"]

        try:
            output["client_certificate_data"] = kcl._user.value[
                "client-certificate-data"
            ]
            output["client_key_data"] = kcl._user.value["client-key-data"]
        except Exception:
            print(
                "client certificate and key data missing, trying to extract"
                " token"
            )

        if (
            "client_key_data" not in output
            and "client_certificate_data" not in output
        ):
            try:
                output["token"] = kcl._user.value["token"]
            except Exception:
                print("token missing for user in kubeconfig")

        if (
            "client_key_data" not in output
            and "client_certificate_data" not in output
            and "token" not in output
        ):
            return "error", ErrorOutput(
                1, "Both client data and token missing, exiting!"
            )

        print(output)

        return "success", kubeconfig_output_schema.unserialize(output)
    except Exception:
        return "error", ErrorOutput(1, "Failure in parsing kubeconfig:")


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                extract_kubeconfig,
            )
        )
    )
