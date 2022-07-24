"""
utils module for lstm library
provides non lstm specific miscellaneous methods
"""

import json
import logging
import time
from dataclasses import asdict
from pathlib import Path
from typing import Dict, List, Tuple

import numpy as np
from sklearn import preprocessing


def strip_forbidden_characters(word: str, characters_dictionary: Dict[str, int]) -> str:
    allowed_characters = [character[0] for character in characters_dictionary]
    word = "".join((filter(lambda char: char in allowed_characters, word)))
    return word


def tokenize_word(word: str, characters_dictionary: Dict[str, int]) -> List[int]:
    """
    breaks a word into individual token units from the characters_dictionary
    @param characters_dictionary: dictionary of tokens
    @param word: word to tokenize
    @return: vector of word tokens
    """
    word_characters = list(word)
    vector: List[int] = [characters_dictionary[_] for _ in word_characters]
    return vector


def remove_prefix(text: str, prefix: str) -> str:
    if text.startswith(prefix):
        return text[len(prefix) :]
    return text


def pad_vector(vector: List[int], desired_length: int) -> List[int]:
    padding = [0] * (desired_length - int(len(vector)))
    return vector[:desired_length] + padding


def separate_domains_that_are_too_long(
    domains: List[str], max_size: int
) -> Tuple[List[str], List[str]]:
    domains_shorter_or_equal = [domain for domain in domains if len(domain) <= max_size]
    domains_too_long = set(domains) - set(domains_shorter_or_equal)
    return domains_shorter_or_equal, list(domains_too_long)


def setup_logging(
    level: str, logformat: str = "%(asctime)2s %(levelname)-8s %(message)s"
):
    numeric_level = getattr(logging, level.upper(), None)
    logging.basicConfig(level=numeric_level, format=logformat)
    logging.debug(f"logging level set to {level}")


def load_labels(encoder_path: Path) -> Dict[int, str]:
    encoder = preprocessing.LabelEncoder()
    encoder.classes_ = np.load(encoder_path)
    labels = dict(zip(range(len(encoder.classes_)), encoder.classes_))
    return labels


def log_analysis(domain) -> None:
    """
    reports to stdout outcome of classification
    """
    logging.info(
        f"{domain.raw}, is_dga: {domain.is_dga}, family: {domain.family_label}"
    )
    for word in domain.words:
        logging.debug(asdict(domain))


def log_performance(counter, start_time):
    elapsed_time = time.time() - start_time
    avg_classification_took = elapsed_time / counter
    logging.warning(
        f"classified {counter} domains, took on average: {avg_classification_took}s"
    )


def pretty_print(domains, output_format="json") -> str:
    dicts = [asdict(domain) for domain in domains]
    for domain in dicts:
        for word in domain["words"]:
            del word["padded_token_vector"]
    if output_format == "json":
        print(json.dumps(dicts, indent=2))
