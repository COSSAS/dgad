import logging
from typing import Optional

import grpc
import redis

from dgad.grpc import classification_pb2, classification_pb2_grpc


class RedisWorker:
    def __init__(
        self,
        redis_host: str,
        redis_port: int,
        redis_set: str,
        grpc_host: str,
        grpc_port: str,
    ):
        self.redis_client = redis.Redis(redis_host, redis_port)
        self.redis_set = redis_set
        self.grpc_host = grpc_host
        self.grpc_port = grpc_port
        self.counter = 0

    def run(self) -> None:
        while True:
            domain = self.__redis_get_domain_to_classify__()
            if domain:
                binary_classification = self.classify_domain(domain)
                self.counter += self.__redis_store_classification__(
                    domain, binary_classification
                )
                if self.counter % 100 == 0:
                    logging.critical(
                        "todo: %s, done: %s",
                        self.redis_client.scard(self.redis_set),
                        self.redis_client.dbsize(),
                    )
                logging.debug("%s: %s", domain, binary_classification)
            else:
                logging.info("waiting for domains...")

    def classify_domain(self, domain: str) -> str:
        with grpc.insecure_channel(f"{self.grpc_host}:{self.grpc_port}") as channel:
            stub = classification_pb2_grpc.ClassifierStub(channel)
            response = stub.GetClassification(
                classification_pb2.Domain(fqdn=domain), wait_for_ready=True
            )
        return str(response.binary_classification)

    def __redis_get_domain_to_classify__(self) -> Optional[str]:
        domain = self.redis_client.spop(name=self.redis_set)
        if domain:
            return str(domain.decode("UTF-8"))
        else:
            return None

    def __redis_store_classification__(
        self, domain: str, binary_classification: str
    ) -> int:
        return int(self.redis_client.set(name=domain, value=binary_classification))  # type: ignore[arg-type]
