import logging
import os

from dgad_redis_worker.worker import RedisWorker

if __name__ == "__main__":
    logging.basicConfig(
        format="%(levelname)s: %(message)s",
        level=os.environ.get(key="LOG_LEVEL", default="ERROR").upper(),
    )
    dgad_grpc_host = os.environ.get("DGAD_GRPC_HOST", "localhost")
    dgad_grpc_port = os.environ.get("DGAD_GRPC_PORT", "50054")
    redis_host = os.environ.get("REDIS_HOST", "localhost")
    redis_port = int(os.environ.get("REDIS_PORT", "6379"))
    redis_set = os.environ.get("REDIS_SET", "domains_todo")

    redis_worker = RedisWorker(
        redis_host=redis_host,
        redis_port=redis_port,
        redis_set=redis_set,
        grpc_host=dgad_grpc_host,
        grpc_port=dgad_grpc_port,
    )

    logging.critical("started dga detective redis worker")
    redis_worker.run()
