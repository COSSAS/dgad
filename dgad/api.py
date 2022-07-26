# type: ignore
# pylint: disable-all

import logging
import time
import uuid
from concurrent import futures

import grpc

from dgad.grpc import prediction_pb2, prediction_pb2_grpc
from dgad.prediction import Detective
from dgad.schema import Domain, Word
from dgad.utils import log_performance


def unpack(response) -> Domain:
    domain = Domain(
        raw=response.fqdn, is_dga=response.is_dga, family_label=response.family
    )
    words = [
        Word(
            value=word.value,
            binary_score=word.binary_score,
            binary_label=word.binary_label,
            family_score=word.family_score,
            family_label=word.family_label,
        )
        for word in response.words
    ]
    domain.words = words
    return domain


def pack(domain: Domain):
    words = [
        prediction_pb2.Word(
            value=word.value,
            binary_score=word.binary_score,
            binary_label=word.binary_label,
            family_score=word.family_score,
            family_label=word.family_label,
        )
        for word in domain.words
    ]
    return prediction_pb2.Domain(
        fqdn=domain.raw,
        is_dga=domain.is_dga,
        family=domain.family_label,
        words=words,
    )


class Classifier(prediction_pb2_grpc.Classifier):
    def __init__(self, detective: Detective):
        self.detective = detective
        self.counter = 0
        self.start_time = time.time()
        self.id = uuid.uuid4()
        logging.warning(f"started dga detective classifier {self.id}")

    def GetClassification(self, request, context):
        raw_domains = [request.fqdn]
        domains, _ = self.detective.prepare_domains(raw_domains)
        self.detective.investigate(domains=domains)
        domain = domains[0]
        self.counter += 1
        if self.counter % 100 == 0:
            log_performance(counter=self.counter, start_time=self.start_time)
        return pack(domain)


class DGADServer:
    def __init__(self, detective: Detective, port: int, max_workers: int):
        self.detective = detective
        self.port = port
        self.max_workers = max_workers

    def bootstrap(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=self.max_workers))
        prediction_pb2_grpc.add_ClassifierServicer_to_server(
            Classifier(self.detective), server
        )
        server.add_insecure_port(f"[::]:{self.port}")
        server.start()
        server.wait_for_termination()


class DGADClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def requests(self, domain: str):
        with grpc.insecure_channel(f"{self.host}:{self.port}") as channel:
            stub = prediction_pb2_grpc.ClassifierStub(channel)
            response = stub.GetClassification(
                prediction_pb2.Domain(fqdn=domain), wait_for_ready=True
            )
            return unpack(response)
