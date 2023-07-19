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
                f" Exception: {e}"
            )

        # Kubeconfig files have the kind set as Config
        try:
            kind = kubeconfig["kind"]
        except KeyError:
            return "error", ErrorOutput(
                "The provided file is not a kubeconfig file (missing 'kind' field)"
            )
        if kind != "Config":
            return "error", ErrorOutput("The provided file is not a kubeconfig file")

        # Get the current context, then search for the values for that context in the
        # context section
        current_context = kubeconfig.get("current-context", None)
        if current_context is None:
            return "error", ErrorOutput(
                "The provided kubeconfig file does not have a current-context set."
                " Please set a current context to use."
            )

        try:
            contexts = kubeconfig["contexts"]
        except KeyError:
            return "error", ErrorOutput("'contexts' field missing from kubeconfig.")

        context = None
        for ctx in contexts:
            try:
                if ctx["name"] == current_context:
                    context = ctx["context"]
            except KeyError as e:
                return "error", ErrorOutput(
                    f"{e} section missing from context entry in kubeconfig"
                )
        if context is None:
            return "error", ErrorOutput(
                f"Failed to find a context named {current_context} in the kubeconfig"
                " file."
            )

        try:
            current_cluster = context["cluster"]
            current_user = context["user"]
        except KeyError as e:
            return "error", ErrorOutput(
                f"{e} field missing from kubeconfig current context"
            )

        # Now find the cluster for that current context
        try:
            clusters = kubeconfig["clusters"]
        except KeyError:
            return "error", ErrorOutput("Clusters section missing from kubeconfig file")

        cluster = None
        for cl in clusters:
            try:
                if cl["name"] == current_cluster:
                    try:
                        cluster = cl["cluster"]
                    except KeyError:
                        return "error", ErrorOutput(
                            "cluster section missing from section of current cluster"
                            f" {current_cluster}"
                        )
            except KeyError as e:
                return "error", ErrorOutput(
                    f"{e} section missing from clusters entry in kubeconfig"
                )
        if cluster is None:
            return "error", ErrorOutput(
                f"Failed to find a cluster named {current_cluster} in the kubeconfig"
                " file."
            )

        # Now find the user for current context's user for authentication.
        try:
            users = kubeconfig["users"]
        except KeyError:
            return "error", ErrorOutput("'users' section not found in kubeconfig")

        user = None
        for u in users:
            try:
                if u["name"] == current_user:
                    user = u["user"]
            except KeyError as e:
                return "error", ErrorOutput(
                    f"{e} section in the users section not found in the kubeconfig"
                )
        if user is None:
            return "error", ErrorOutput(
                f"Failed to find a user named {current_user} in the kubeconfig file."
            )

        # Ensure the server is in the kubeconfig
        try:
            server = cluster["server"]
        except KeyError:
            return "error", ErrorOutput(
                f"Failed to find server in cluster kubeconfig file {current_cluster}"
                " cluster section"
            )
        # Populate output values from the user and server sections.
        output = SuccessOutput(
            Connection(host=server),
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
        return "error", ErrorOutput(
            f"Failure to parse kubeconfig. Exception: {e}. Traceback: "
            + traceback.format_exc()
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
