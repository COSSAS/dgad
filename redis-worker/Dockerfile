FROM python:slim
RUN apt update && apt install git -y
WORKDIR /project
COPY dgad_redis_worker dgad_redis_worker
COPY pyproject.toml .
RUN pip install .

CMD python /project/dgad_redis_worker/run.py
