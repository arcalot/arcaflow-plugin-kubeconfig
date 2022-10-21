FROM quay.io/centos/centos:stream8

RUN dnf -y module install python39 && dnf -y install --setopt=tsflags=nodocs python39 python39-pip git && dnf clean all
RUN mkdir /app
ADD https://raw.githubusercontent.com/arcalot/arcaflow-plugins/main/LICENSE /app/
ADD kubeconfig_plugin.py /app/
ADD test_kubeconfig_plugin.py /app/
ADD poetry.lock pyproject.toml /app/
ADD tests /app/tests/
WORKDIR /app

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --without dev

RUN mkdir /htmlcov
RUN pip3 install coverage
RUN python3 -m coverage run test_kubeconfig_plugin.py
RUN python3 -m coverage html -d /htmlcov

VOLUME /config

ENTRYPOINT ["python3.9", "/app/kubeconfig_plugin.py"]
CMD []

LABEL org.opencontainers.image.source="https://github.com/arcalot/arcaflow-plugin-kubeconfig"
LABEL org.opencontainers.image.licenses="Apache-2.0+GPL-2.0-only"
LABEL org.opencontainers.image.vendor="Arcalot project"
LABEL org.opencontainers.image.authors="Arcalot contributors"
LABEL org.opencontainers.image.title="Kubeconfig Python Plugin"
LABEL io.github.arcalot.arcaflow.plugin.version="1"