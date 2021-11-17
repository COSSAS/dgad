FROM python:3.9
RUN pip install poetry
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /project
COPY poetry.lock pyproject.toml ./
COPY dgad/__init__.py dgad/__init__.py
RUN poetry install --no-dev

COPY dgad/ dgad/
RUN dgad --help

ENV TF_CPP_MIN_LOG_LEVEL=3
ENTRYPOINT [ "dgad"]
CMD [ "-h" ]
