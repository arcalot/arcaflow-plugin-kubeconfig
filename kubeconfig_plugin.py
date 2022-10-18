#!/usr/bin/env python3
import base64
import sys
import traceback
import typing
from dataclasses import dataclass, field
from arcaflow_plugin_sdk import plugin, validation, schema
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
        schema.description("Server name to verify TLS certificate against.")
    ] = None
    cert: typing.Annotated[
        typing.Optional[str],
        schema.name("Client certificate"),
        schema.description("Client cert data in PEM format"),
    ] = None
    key: typing.Annotated[
        typing.Optional[str],
        schema.name("Client key"),
        schema.description("Client key in PEM format")
    ] = None
    cacert: typing.Annotated[
        typing.Optional[str],
        schema.name("CA certificate"),
        schema.description("CA certificate in PEM format")
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
        schema.description("Kubernetes connection confirmation.")
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

        try:
            if kubeconfig["kind"] != "Config":
                return "error", ErrorOutput("The provided file is not a kubeconfig file")
        except KeyError:
            return "error", ErrorOutput("The provided file is not a kubeconfig file (missing 'kind' field)")

        try:
            current_context = kubeconfig["current-context"]
        except KeyError:
            return "error", ErrorOutput(
                "The provided kubeconfig file does not have a current-context set. Please set a current context to use.")

        try:
            context = None
            for ctx in kubeconfig["contexts"]:
                if ctx["name"] == current_context:
                    context = ctx["context"]
            if context is None:
                return "error", ErrorOutput(
                    "Failed to find a context named {} in the kubeconfig file.".format(current_context))
            current_cluster = context["cluster"]
            current_user = context["user"]
        except Exception as e:
            return "error", ErrorOutput(
                "Failed to find a context named {} in the kubeconfig file: {}".format(current_context, e.__str__()))

        try:
            cluster = None
            for cl in kubeconfig["clusters"]:
                if cl["name"] == current_cluster:
                    cluster = cl["cluster"]
            if cluster is None:
                return "error", ErrorOutput(
                    "Failed to find a cluster named {} in the kubeconfig file.".format(current_cluster))
        except Exception as e:
            return "error", ErrorOutput(
                "Failed to find a cluster named {} in the kubeconfig file: {}".format(current_cluster, e.__str__()))

        try:
            user = None
            for u in kubeconfig["users"]:
                if u["name"] == current_user:
                    user = u["user"]
            if user is None:
                return "error", ErrorOutput(
                    "Failed to find a user named {} in the kubeconfig file.".format(current_user))
        except Exception as e:
            return "error", ErrorOutput(
                "Failed to find a user named {} in the kubeconfig file: {}".format(current_user, e.__str__()))

        output = SuccessOutput(
            Connection(host=cluster["server"]),
        )
        try:
            output.connection.cacert = base64.b64decode(cluster[
                                                            "certificate-authority-data"
                                                        ]).decode('ascii')
        except KeyError:
            pass
        try:
            output.connection.cert = base64.b64decode(user[
                                                          "client-certificate-data"
                                                      ]).decode('ascii')
        except KeyError:
            pass
        try:
            output.connection.key = base64.b64decode(user[
                                                         "client-key-data"
                                                     ]).decode('ascii')
        except KeyError:
            pass
        try:
            output.connection.username = user["username"]
        except KeyError:
            pass
        try:
            output.connection.password = user["password"]
        except KeyError:
            pass
        try:
            output.connection.bearerToken = user["token"]
        except KeyError:
            pass

        return "success", output
    except Exception as e:
        print(traceback.format_exc())
        return "error", ErrorOutput("Failure to parse kubeconfig: {}".format(e.__str__()))


if __name__ == "__main__":
    sys.exit(
        plugin.run(
            plugin.build_schema(
                extract_kubeconfig,
            )
        )
    )
