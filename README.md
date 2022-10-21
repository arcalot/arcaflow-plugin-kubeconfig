# Kubeconfig Plugin for Arcaflow

The Kubeconfig plugin is used to input a kubernetes or openshift kubeconfig file and parse and extract components of the kubeconfig file
such as cluster name, user, server url, client certificate, client token etc.

The plugin expects a kubeconfig inputed as a string, as defined in the `InputParams` dataclass in [kubeconfig_plugin.py](kubeconfig_plugin.py) file.
You define your test parameters in a YAML file to be passed to the plugin command as shown in [kubeconfig_example.yaml](kubeconfig_example.yaml).

## To test:

In order to run the [kubeconfig plugin](kubeconfig_plugin.py) run the following steps:

### Containerized
1. Clone this repository
2. Create the container with `docker build -t arca-kubeconfig -f Dockerfile`
3. Run `cat kubeconfig_example.yaml | docker run -i arca-kubeconfig -f -` to run the plugin


### Native

1. Clone this repository
2. Create a `venv` in the current directory with `python3 -m venv $(pwd)/venv`
3. Activate the `venv` by running `source venv/bin/activate`
4. Run `pip install poetry`
5. Run `poetry install`
6. Run `./kubeconfig_plugin.py -f kubeconfig_example.yaml ` to run the plugin


## Image Building

You can change this plugin's image version tag in
`.github/workflows/carpenter.yaml` by editing the
`IMAGE_TAG` variable, and pushing that change to the
branch designated in that workflow.
