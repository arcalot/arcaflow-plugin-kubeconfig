#!/usr/bin/env python3
import base64
import sys
import traceback
import typing
from dataclasses import dataclass, field

import yaml
from arcaflow_plugin_sdk import plugin, schema, validation


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
class Connection:
    """
    This is a connection specification matching the Go connection structure.
    """

    host: typing.Annotated[
        str,
        schema.name("Server"),
        schema.description("Kubernetes API URL"),
    ]
    path: typing.Annotated[
        typing.Optional[str],
        schema.name("API path"),
        schema.description("Kubernetes API path"),
    ] = None
    username: typing.Annotated[
        typing.Optional[str],
        schema.name("Username"),
        schema.description("Username to authenticate with."),
    ] = None
    password: typing.Annotated[
        typing.Optional[str],
        schema.name("Password"),
        schema.description("Password to authenticate with."),
    ] = None
    serverName: typing.Annotated[
        typing.Optional[str],
        schema.name("TLS server name"),
        schema.description("Server name to verify TLS certificate against."),
    ] = None
    cert: typing.Annotated[
        typing.Optional[str],
        schema.name("Client certificate"),
        schema.description("Client cert data in PEM format"),
    ] = None
    key: typing.Annotated[
        typing.Optional[str],
        schema.name("Client key"),
        schema.description("Client key in PEM format"),
    ] = None
    cacert: typing.Annotated[
        typing.Optional[str],
        schema.name("CA certificate"),
        schema.description("CA certificate in PEM format"),
    ] = None
    bearerToken: typing.Annotated[
        typing.Optional[str],
        schema.name("Token"),
        schema.description("Secret token of the user/service account"),
    ] = None


@dataclass
class SuccessOutput:
    """
    This is the output data structure for the success case.
    """

    connection: typing.Annotated[
        Connection,
        schema.name("Kubernetes connection"),
        schema.description("Kubernetes connection confirmation."),
    ]


@dataclass
class ErrorOutput:
    """
    This is the output data structure in the error case.
    """

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
        "Inputs a kubeconfig, parses it and extracts the kubernetes cluster details"
    ),
    outputs={"success": SuccessOutput, "error": ErrorOutput},
)
def extract_kubeconfig(
    params: InputParams,
) -> typing.Tuple[str, typing.Union[SuccessOutput, ErrorOutput]]:
    print("==>> Parsing and extracting kubernetes cluster details ...")

    try:
        try:
            kubeconfig = yaml.safe_load(params.kubeconfig)
        except Exception as e:
            return "error", ErrorOutput(
                "Exception occurred while loading YAML. Input is not valid YAML."
                + " Exception: {}".format(e.__str__())
            )

        # Kubeconfig files have the kind set as Config
        if "kind" in kubeconfig:
            if kubeconfig["kind"] != "Config":
                return "error", ErrorOutput(
                    "The provided file is not a kubeconfig file"
                )
        else:
            return "error", ErrorOutput(
                "The provided file is not a kubeconfig file (missing 'kind' field)"
            )

        # Get the current context, then search for the values for that context in the
        # context section
        current_context = kubeconfig.get("current-context", None)
        if current_context is None:
            return "error", ErrorOutput(
                """The provided kubeconfig file does not have a current-context set."""
                """ Please set a current context to use."""
            )

        if "contexts" not in kubeconfig:
            return "error", ErrorOutput("'contexts' field missing from kubeconfig.")

        context = None
        for ctx in kubeconfig["contexts"]:
            if "name" not in ctx:
                return "error", ErrorOutput(
                    "'name' section missing from context entry in kubeconfig"
                )
            if ctx["name"] == current_context:
                context = ctx["context"]
        if context is None:
            return "error", ErrorOutput(
                "Failed to find a context named {} in the kubeconfig file.".format(
                    current_context
                )
            )

        for expected_key in ["cluster", "user"]:
            if expected_key not in context:
                return "error", ErrorOutput(
                    "'{}' field missing from kubeconfig current context.".format(
                        expected_key
                    )
                )
        current_cluster = context["cluster"]
        current_user = context["user"]

        # Now find the cluster for that current context
        if "clusters" not in kubeconfig:
            return "error", ErrorOutput("Clusters section missing from kubeconfig file")

        cluster = None
        for cl in kubeconfig["clusters"]:
            if "name" not in cl:
                return "error", ErrorOutput(
                    "'name' section missing from clusters entry in kubeconfig"
                )
            if cl["name"] == current_cluster:
                if "cluster" not in cl:
                    return "error", ErrorOutput(
                        "cluster section missing from section "
                        + "of current cluster {}".format(current_cluster)
                    )
                cluster = cl["cluster"]
        if cluster is None:
            return "error", ErrorOutput(
                "Failed to find a cluster named {} in the kubeconfig file.".format(
                    current_cluster
                )
            )

        # Now find the user for current context's user for authentication.
        if "users" not in kubeconfig:
            return "error", ErrorOutput("'users' section not found in kubeconfig")
        user = None
        for u in kubeconfig["users"]:
            for required_key in ["name", "user"]:
                if required_key not in u:
                    return "error", ErrorOutput(
                        """'{0}' section in the users section not found in the """
                        """kubeconfig""".format(required_key)
                    )
            if u["name"] == current_user:
                user = u["user"]
        if user is None:
            return "error", ErrorOutput(
                "Failed to find a user named {} in the kubeconfig file.".format(
                    current_user
                )
            )

        # Ensure the server is in the kubeconfig
        if "server" not in cluster:
            return "error", ErrorOutput(
                """Failed to find server in cluster kubeconfig file {0}"""
                """ cluster section""".format(current_cluster)
            )
        # Populate output values from the user and server sections.
        output = SuccessOutput(
            Connection(host=cluster["server"]),
        )
        output.connection.cacert = base64_decode(
            cluster.get("certificate-authority-data", None)
        )
        output.connection.cert = base64_decode(
            user.get("client-certificate-data", None)
        )
        output.connection.key = base64_decode(user.get("client-key-data", None))
        output.connection.username = user.get("username", None)
        output.connection.password = user.get("password", None)
        output.connection.bearerToken = user.get("token", None)

        return "success", output
    except Exception as e:
        # This is the catch-all case.
        # The goal is for all other errors to be addressed individually.
        print(traceback.format_exc())
        return "error", ErrorOutput(
            "Failure to parse kubeconfig. Exception: {}".format(e.__str__())
        )


def base64_decode(encoded):
    if encoded is None:
        return None
    return base64.b64decode(encoded).decode("ascii")


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                extract_kubeconfig,
            )
        )
    )
