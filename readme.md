# DGA Detective v3.0.4

* Python package to perform DGA domain classification
* Can be used:
  - as a python package
  - locally, through CLI
  - remotely, through gRPC
* Classifcation methods:
  - [TCN](https://github.com/philipperemy/keras-tcn)
  - LSTM

## Installation
```bash
# recommended: use a virtual environment
python -m venv dgad
source dgad/bin/activate
pip install git+https://gitlab.com/cossas/dgad.git
```

## CLI

```bash
# display help
$ dgad --help
# classify one domain
$ dgad --domain wikipedia.org
          domain classification
0  wikipedia.org             ok
# classify several domains
$ dgad --domains wikipedia.org ksadjfhlasdkjfsakjdf.com
                     domain classification
0             wikipedia.org             ok
1  ksadjfhlasdkjfsakjdf.com            DGA
# classify from/to a csv file
$ dgad --csv your_csv_file.csv
```

## gRPC micro server

* Server
  ```bash
  # listens by default on port 50054
  python dgad/grpc/classifier_server.py
  # you can override default logging and port like this
  LOG_LEVEL=info LISTENING_PORT=55666 python dgad/grpc/classifier_server.py
  ```

* Client
  ```bash
  # an example client is provided at dgad/grpc/classifier_client.py
  python dgad/grpc/classifier_client.py
  # you can override default destination host and port like this
  GRPC_HOST=x.x.x.x GRPC_PORT=55666 python dgad/grpc/classifier_client.py
  ```

## Development

Requirements:
* python >= 3.7
* [poetry](https://python-poetry.org)

```bash
git clone 
cd dga-detective
# install project, poetry will spawn a new venv
poetry install
# (optional) install pre-commit hooks
pre-commit install
pre-commit install --hook-type commit-msg

# gRPC code generation
python -m grpc_tools.protoc -I dgad/grpc/protos --python_out=dgad/grpc --grpc_python_out=dgad/grpc dgad/grpc/protos/classification.proto
```

## About

DGA Detective is developed in the SOCCRATES innovation project (https://soccrates.eu). SOCCRATES has received funding from the European Union’s Horizon 2020 Research and Innovation program under Grant Agreement No. 833481.
