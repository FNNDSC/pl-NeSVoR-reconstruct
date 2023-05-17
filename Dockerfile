FROM docker.io/junshenxu/nesvor:v0.4.0

WORKDIR /usr/local/src/app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ARG extras_require=none
RUN pip install ".[${extras_require}]"

CMD ["nesvor_reconstruct"]