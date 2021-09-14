FROM python:3.9-slim
WORKDIR /project
COPY pyproject.toml .
COPY dgad dgad
RUN pip install .
COPY tests/*.py tests/
COPY tests/data tests/data
ENV TF_CPP_MIN_LOG_LEVEL=3
ENTRYPOINT [ "dgad"]
CMD [ "-h" ]
