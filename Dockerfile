FROM python:3.10-slim as builder
WORKDIR /project
COPY pyproject.toml .
COPY dgad dgad
RUN pip install --prefix=/install .

FROM python:3.10-slim
COPY --from=builder /install /usr/local
WORKDIR /project
COPY dgad dgad
COPY tests/*.py tests/
COPY tests/data tests/data
ENV TF_CPP_MIN_LOG_LEVEL=3
ENTRYPOINT [ "dgad"]
CMD [ "-h" ]
