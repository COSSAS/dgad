# type: ignore

import logging
import os
import random
import string

import grpc

from dgad.grpc import classification_pb2, classification_pb2_grpc


def run():

    domains = []
    amount = int(os.environ.get("AMOUNT", 10000))
    for _ in range(amount):
        domain = "".join(
            random.choice(string.ascii_lowercase) for _ in range(20)  # nosec
        )
        domains.append(domain + ".com")
    logging.critical("created %s random domains", amount)

    host = os.environ.get("GRPC_HOST", "localhost")
    port = os.environ.get("GRPC_PORT", "50054")

    with grpc.insecure_channel(f"{host}:{port}") as channel:
        for domain in domains:
            stub = classification_pb2_grpc.ClassifierStub(channel)
            response = stub.GetClassification(
                classification_pb2.Domain(fqdn=domain), wait_for_ready=True
            )
            logging.critical("%s %s", response.fqdn, response.binary_classification)


if __name__ == "__main__":
    logging.basicConfig()
    run()
