test:
	python dgad/cli.py -ft csv -f tests/data/domains_todo.csv
	python dgad/cli.py -f tests/data/domains_todo.csv
	python dgad/cli.py -ft jsonl -f tests/data/domains_todo.jsonl
	cat tests/data/domains_todo.csv | python dgad/cli.py -ft csv -f -
	cat tests/data/domains_todo.jsonl | python dgad/cli.py -ft jsonl -f -

clean:
	black .
	isort --profile=black .

protoc:
	python -m grpc_tools.protoc -I protos --python_out=dgad/grpc --grpc_python_out=dgad/grpc prediction.proto
