FROM python:3.9-slim
RUN pip install poetry
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /project
COPY poetry.lock pyproject.toml ./
COPY dgad_redis_worker/__init__.py dgad_redis_worker/__init__.py
RUN poetry install --no-dev

COPY dgad_redis_worker/ dgad_redis_worker/
ENV TF_CPP_MIN_LOG_LEVEL=3
CMD python /project/dgad_redis_worker/run.py
