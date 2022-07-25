test:
	docker build -t dgad:test .
	cat demo/domains.csv | docker run -i dgad:test client -fmt csv -f - | jq '{domain: .[0].raw, is_dga: .[0].is_dga}'
	cat demo/domains.jsonl | docker run -i dgad:test client -fmt jsonl -f - | jq '{domain: .[0].raw, is_dga: .[0].is_dga}'
	cat demo/domains.txt | docker run -i dgad:test client -fmt txt -f - | jq '{domain: .[0].raw, is_dga: .[0].is_dga}'

clean:
	black .
	isort --profile=black .

protoc:
	python -m grpc_tools.protoc -I protos --python_out=dgad/grpc --grpc_python_out=dgad/grpc prediction.proto
