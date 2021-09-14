# type: ignore

import logging
import os
import random
import string
from typing import List

import redis


def generate_dga_domains(amount: int) -> List[str]:
    domains = []
    for _ in range(amount):
        domain = "".join(
            random.choice(string.ascii_lowercase) for _ in range(20)  # nosec
        )
        domains.append(domain + ".com")
    return domains


if __name__ == "__main__":
    amount = int(os.environ.get("AMOUNT", 1000))
    redis_host = os.environ.get("REDIS_HOST", "redis")
    redis_port = os.environ.get("REDIS_PORT", "6379")
    domains = generate_dga_domains(amount=amount)
    redis_client = redis.Redis(host=redis_host, port=redis_port)
    amount_inserted = sum(
        redis_client.sadd("domains_todo", domain) for domain in domains
    )
    logging.critical("added %s domains to redis set", amount_inserted)
