FROM python:3.9-slim

WORKDIR /project
COPY pyproject.toml ./
COPY dgad/ dgad/
RUN pip --disable-pip-version-check install --no-compile  .
RUN dgad --help

ENV TF_CPP_MIN_LOG_LEVEL=3
ENTRYPOINT [ "dgad"]
CMD [ "--help" ]
