# type: ignore

import logging
import os
import random
import string
import time
from concurrent import futures
from importlib import resources

import grpc

import dgad.models
from dgad.classification import TCNClassifier
from dgad.grpc import classification_pb2, classification_pb2_grpc


class Classifier(classification_pb2_grpc.Classifier):
    def __init__(self):
        self.classifier = TCNClassifier()
        with resources.path(dgad.models, "tcn_best.h5") as model_path:
            self.classifier.load_keras_model(filepath=model_path)
        self.counter = 0
        self.start_interval_time = time.time()
        self.interval_size = 100
        self.id = "".join(random.choice(string.digits) for _ in range(5))  # nosec
        logging.critical("started dga detective classifier %s", self.id)

    def GetClassification(self, request, context):
        classified_domain = self.classifier.classify_raw_domains(
            raw_domains=[request.fqdn]
        )[0]
        self.counter += 1
        if self.counter % self.interval_size == 0:
            logging.info(
                "%s: classified %s domains in %s",
                self.id,
                self.interval_size,
                time.time() - self.start_interval_time,
            )
            self.start_interval_time = time.time()
        return classification_pb2.Classification(
            fqdn=request.fqdn,
            binary_classification=classified_domain.binary_label,
        )


def serve():
    port = os.environ.get("LISTENING_PORT", 50054)
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    classification_pb2_grpc.add_ClassifierServicer_to_server(Classifier(), server)
    server.add_insecure_port(f"[::]:{port}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=os.environ.get(key="LOG_LEVEL", default="ERROR").upper(),
    )
    serve()
