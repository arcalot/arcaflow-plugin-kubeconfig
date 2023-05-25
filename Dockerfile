ARG package=arcaflow_plugin_kubeconfig

# build poetry
FROM quay.io/centos/centos:stream8 as poetry
ARG package
RUN dnf module -y install python39 && dnf -y install python39 python39-pip

WORKDIR /app

COPY poetry.lock /app/
COPY pyproject.toml /app/
COPY ${package}/ /app/${package}
COPY README.md /app/

# python3.9 -c "import certifi; print(certifi.where())"
# /usr/local/lib/python3.9/site-packages/certifi/cacert.pem

RUN python3.9 -m pip install poetry \
# FIX per https://github.com/python-poetry/poetry/issues/5977
 && python3.9 -m poetry add certifi \
 && python3.9 -m poetry config virtualenvs.create false \
#  && python3.9 -c "import certifi; print(certifi.where())" \
#  && poetry config certificates.certifi.cert /usr/local/lib/python3.9/site-packages/certifi/cacert.pem \
 && python3.9 -m poetry install \
 && python3.9 -m poetry export -f requirements.txt --output requirements.txt --without-hashes

# run tests
COPY tests /app/tests

RUN mkdir /htmlcov
RUN pip3 install coverage
RUN python3 -m coverage run tests/test_kubeconfig_plugin.py
RUN python3 -m coverage html -d /htmlcov --omit=/usr/local/*

# final image
FROM quay.io/centos/centos:stream8
ARG package
RUN dnf module -y install python39 && dnf -y install python39 python39-pip

WORKDIR /app

COPY --from=poetry /app/requirements.txt /app/
COPY --from=poetry /htmlcov /htmlcov/
COPY LICENSE /app/
COPY README.md /app/
COPY ${package}/ /app/${package}

RUN python3.9 -m pip install -r requirements.txt

WORKDIR /app/${package}

ENTRYPOINT ["python3", "kubeconfig_plugin.py"]
CMD []




# RUN dnf -y module install python39 && dnf -y install --setopt=tsflags=nodocs python39 python39-pip git && dnf clean all
# RUN mkdir /app
# ADD https://raw.githubusercontent.com/arcalot/arcaflow-plugins/main/LICENSE /app/
# ADD kubeconfig_plugin.py /app/
# ADD test_kubeconfig_plugin.py /app/
# ADD poetry.lock pyproject.toml /app/
# ADD tests /app/tests/
# WORKDIR /app

# RUN pip3 install poetry
# RUN poetry config virtualenvs.create false
# RUN poetry install

# RUN mkdir /htmlcov
# RUN pip3 install coverage
# RUN python3 -m coverage run test_kubeconfig_plugin.py
# RUN python3 -m coverage html -d /htmlcov

# VOLUME /config

# ENTRYPOINT ["python3.9", "/app/kubeconfig_plugin.py"]
# CMD []

LABEL org.opencontainers.image.source="https://github.com/arcalot/arcaflow-plugin-kubeconfig"
LABEL org.opencontainers.image.licenses="Apache-2.0+GPL-2.0-only"
LABEL org.opencontainers.image.vendor="Arcalot project"
LABEL org.opencontainers.image.authors="Arcalot contributors"
LABEL org.opencontainers.image.title="Kubeconfig Python Plugin"
LABEL io.github.arcalot.arcaflow.plugin.version="1"
