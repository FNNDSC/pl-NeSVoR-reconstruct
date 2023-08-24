FROM docker.io/fnndsc/nesvor:v0.6.0rc2

WORKDIR /usr/local/src/pl-nesvor

COPY setup.py nesvor_wrapper.py ./
ARG extras_require=none
RUN pip install ".[${extras_require}]"

WORKDIR /
CMD ["nesvor_reconstruct"]
